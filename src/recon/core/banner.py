"""Módulo para el grabbing de banners de servicios de red."""

import asyncio
import re

from recon.config import logger


def sanitizar_banner(banner: str) -> str:
    """Sanitiza el banner capturado para eliminar caracteres no imprimibles.

    Args:
        banner: El string crudo capturado del socket.

    Returns:
        String sanitizado y sin saltos de línea innecesarios.
    """
    # Eliminar caracteres no imprimibles excepto espacios básicos
    sanitizado = "".join(
        char for char in banner if char.isprintable() or char in "\t\n\r"
    )
    # Reemplazar múltiples espacios y saltos de línea por un solo espacio
    sanitizado = re.sub(r"\s+", " ", sanitizado).strip()
    return sanitizado


async def capturar_banner(host: str, puerto: int, timeout: float = 2.0) -> str | None:
    """Intenta capturar el banner de un servicio en un puerto abierto.

    Args:
        host: Host objetivo.
        puerto: Puerto abierto.
        timeout: Tiempo máximo total para la operación.

    Returns:
        El banner sanitizado o None si no se pudo obtener.
    """

    async def _logic() -> str | None:
        reader, writer = await asyncio.open_connection(host, puerto)
        try:
            # Timeout reducido para la lectura (la mitad del total)
            read_timeout = timeout / 2
            data = await asyncio.wait_for(reader.read(1024), timeout=read_timeout)
            banner = data.decode("utf-8", errors="ignore")
            if banner:
                return sanitizar_banner(banner)
            return None
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass

    try:
        return await asyncio.wait_for(_logic(), timeout=timeout)
    except (asyncio.TimeoutError, ConnectionError, OSError) as e:
        logger.debug("Error capturando banner en %s:%d: %s", host, puerto, e)
    except Exception as e:
        logger.exception("Error inesperado capturando banner en %s:%d", host, puerto)

    return None
