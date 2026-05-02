"""Module for network service banner grabbing."""

import asyncio
import re

from recon.config import logger


def sanitizar_banner(banner: str) -> str:
    """Sanitizes the captured banner to remove non-printable characters.

    Args:
        banner: The raw string captured from the socket.

    Returns:
        Sanitized string without unnecessary line breaks.
    """
    # Remove non-printable characters except basic spaces
    sanitizado = "".join(
        char for char in banner if char.isprintable() or char in "\t\n\r"
    )
    # Replace multiple spaces and line breaks with a single space
    sanitizado = re.sub(r"\s+", " ", sanitizado).strip()
    return sanitizado


async def capturar_banner(host: str, puerto: int, timeout: float = 2.0) -> str | None:
    """Attempts to capture the banner of a service on an open port.

    Args:
        host: Target host.
        puerto: Open port.
        timeout: Maximum total time for the operation.

    Returns:
        The sanitized banner or None if it could not be obtained.
    """

    async def _logic() -> str | None:
        reader, writer = await asyncio.open_connection(host, puerto)
        try:
            # Reduced timeout for reading (half of the total)
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
        logger.debug("Error capturing banner at %s:%d: %s", host, puerto, e)
    except Exception as e:
        logger.exception("Unexpected error capturing banner at %s:%d", host, puerto)

    return None
