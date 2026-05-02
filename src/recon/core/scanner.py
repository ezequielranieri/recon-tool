"""Port scanning logic using asyncio."""

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
    """Scans a specific port asynchronously.

    Args:
        host: Target IP address or hostname.
        puerto: Port number (1-65535).
        timeout: Maximum wait time in seconds.
        semaforo: Semaphore to limit concurrency.

    Returns:
        A ResultadoPuerto object with the detected details.
    """
    if timeout is None:
        timeout = settings.timeout_default

    start_time = time.monotonic()

    # Semaphore context if provided
    if semaforo:
        async with semaforo:
            return await _realizar_escaneo(host, puerto, timeout, start_time)

    return await _realizar_escaneo(host, puerto, timeout, start_time)


async def _realizar_escaneo(
    host: str, puerto: int, timeout: float, start_time: float
) -> ResultadoPuerto:
    """Performs the socket connection in a non-blocking way."""
    try:
        # We attempt to open a TCP connection
        future = asyncio.open_connection(host, puerto)
        reader, writer = await asyncio.wait_for(future, timeout=timeout)

        # If we get here, the port is open
        writer.close()
        await writer.wait_closed()
        estado = "open"

    except TimeoutError:
        # Timeout usually indicates that the port is filtered (drop)
        estado = "filtered"
    except (ConnectionRefusedError, socket.gaierror):
        # Connection explicitly refused or host error
        estado = "closed"
    except OSError:
        # Other network errors
        estado = "closed"
    except Exception as e:
        logger.debug("Unexpected error scanning %s:%d: %s", host, puerto, e)
        estado = "closed"

    end_time = time.monotonic()
    duracion_ms = (end_time - start_time) * 1000

    return ResultadoPuerto(
        puerto=puerto, estado=estado, tiempo_ms=round(duracion_ms, 2)
    )


async def escanear_rango(
    host: str, puertos: list[int], max_workers: int = 100, timeout: float = 1.0
) -> list[ResultadoPuerto]:
    """Scans a set of ports concurrently.

    Args:
        host: The target host.
        puertos: List of ports to scan.
        max_workers: Concurrent connections limit.
        timeout: Timeout per port.

    Returns:
        List of results for each port.
    """
    semaforo = asyncio.Semaphore(max_workers)
    tareas = [escanear_puerto(host, p, timeout, semaforo) for p in puertos]

    return await asyncio.gather(*tareas)
