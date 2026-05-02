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
        timeout: Tiempo máximo de espera para la respuesta del servicio.

    Returns:
        El banner sanitizado o None si no se pudo obtener.
    """
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, puerto), timeout=timeout
        )

        # Intentamos leer lo que el servicio envía al conectar
        try:
            # Leemos hasta 1024 bytes
            data = await asyncio.wait_for(reader.read(1024), timeout=timeout)
            banner = data.decode("utf-8", errors="ignore")

            writer.close()
            await writer.wait_closed()

            if banner:
                return sanitizar_banner(banner)
        except (TimeoutError, ConnectionError):
            writer.close()
            await writer.wait_closed()
            return None

    except Exception as e:
        logger.debug("Error capturando banner en %s:%d: %s", host, puerto, e)

    return None
