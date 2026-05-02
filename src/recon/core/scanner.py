"""Lógica de escaneo de puertos utilizando asyncio."""

import asyncio
import socket
import time

from recon.config import logger, settings
from recon.core.models import ResultadoPuerto


async def escanear_puerto(
    host: str,
    puerto: int,
    timeout: float | None = None,
    semaforo: asyncio.Semaphore | None = None,
) -> ResultadoPuerto:
    """Escanea un puerto específico de forma asíncrona.

    Args:
        host: Dirección IP o hostname del objetivo.
        puerto: Número del puerto (1-65535).
        timeout: Tiempo máximo de espera en segundos.
        semaforo: Semáforo para limitar la concurrencia.

    Returns:
        Un objeto ResultadoPuerto con los detalles detectados.
    """
    if timeout is None:
        timeout = settings.timeout_default

    start_time = time.monotonic()

    # Contexto del semáforo si se proporciona
    if semaforo:
        async with semaforo:
            return await _realizar_escaneo(host, puerto, timeout, start_time)

    return await _realizar_escaneo(host, puerto, timeout, start_time)


async def _realizar_escaneo(
    host: str, puerto: int, timeout: float, start_time: float
) -> ResultadoPuerto:
    """Realiza la conexión socket de forma no bloqueante."""
    try:
        # Intentamos abrir una conexión TCP
        future = asyncio.open_connection(host, puerto)
        reader, writer = await asyncio.wait_for(future, timeout=timeout)

        # Si llegamos aquí, el puerto está abierto
        writer.close()
        await writer.wait_closed()
        estado = "abierto"

    except TimeoutError:
        # Timeout suele indicar que el puerto está filtrado (drop)
        estado = "filtrado"
    except (ConnectionRefusedError, socket.gaierror):
        # Conexión rechazada explícitamente o error de host
        estado = "cerrado"
    except OSError:
        # Otros errores de red
        estado = "cerrado"
    except Exception as e:
        logger.debug("Error inesperado escaneando %s:%d: %s", host, puerto, e)
        estado = "cerrado"

    end_time = time.monotonic()
    duracion_ms = (end_time - start_time) * 1000

    return ResultadoPuerto(
        puerto=puerto, estado=estado, tiempo_ms=round(duracion_ms, 2)
    )


async def escanear_rango(
    host: str, puertos: list[int], max_workers: int = 100, timeout: float = 1.0
) -> list[ResultadoPuerto]:
    """Escanea un conjunto de puertos concurrentemente.

    Args:
        host: El host objetivo.
        puertos: Lista de puertos a escanear.
        max_workers: Límite de conexiones simultáneas.
        timeout: Tiempo de espera por puerto.

    Returns:
        Lista de resultados para cada puerto.
    """
    semaforo = asyncio.Semaphore(max_workers)
    tareas = [escanear_puerto(host, p, timeout, semaforo) for p in puertos]

    return await asyncio.gather(*tareas)
