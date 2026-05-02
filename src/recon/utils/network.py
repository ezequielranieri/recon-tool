"""Low-level network utilities and safe socket handling."""

import socket
import ssl
from typing import Any


def conectar_seguro(
    host: str, puerto: int, timeout: float = 3.0, use_ssl: bool = False
) -> socket.socket:
    """Creates a socket connection with safe resource management.

    Args:
        host: Target hostname or IP.
        puerto: Port to connect to.
        timeout: Maximum wait time in seconds.
        use_ssl: Whether to apply an SSL/TLS layer.

    Returns:
        Connected socket.

    Raises:
        ConnectionError: If the connection cannot be established.
        ValueError: If parameters are invalid.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        if use_ssl:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)

        sock.connect((host, puerto))
        return sock
    except socket.timeout:
        sock.close()
        raise ConnectionError(f"Timeout connecting to {host}:{puerto}")
    except OSError as e:
        sock.close()
        raise ConnectionError(f"Could not connect to {host}:{puerto}: {e}") from e
    except Exception as e:
        sock.close()
        raise ConnectionError(f"Unexpected error connecting to {host}:{puerto}: {e}")


def es_puerto_abierto(host: str, puerto: int, timeout: float = 1.0) -> bool:
    """Quick check if a port is open (without keeping the connection).

    Args:
        host: Target host.
        puerto: Port to verify.
        timeout: Maximum wait time.

    Returns:
        True if the port accepted the connection, False otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        resultado = sock.connect_ex((host, puerto))
        return resultado == 0
