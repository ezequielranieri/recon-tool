"""Utilidades de red de bajo nivel y manejo seguro de sockets."""

import socket
import ssl
from typing import Any


def conectar_seguro(
    host: str, puerto: int, timeout: float = 3.0, use_ssl: bool = False
) -> socket.socket:
    """Crea una conexión socket con manejo seguro de recursos.

    Args:
        host: Hostname o IP objetivo.
        puerto: Puerto a conectar.
        timeout: Tiempo máximo de espera en segundos.
        use_ssl: Si se debe aplicar una capa SSL/TLS.

    Returns:
        Socket conectado.

    Raises:
        ConnectionError: Si no se puede establecer la conexión.
        ValueError: Si los parámetros son inválidos.
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
        raise ConnectionError(f"Timeout conectando a {host}:{puerto}")
    except OSError as e:
        sock.close()
        raise ConnectionError(f"No se pudo conectar a {host}:{puerto}: {e}") from e
    except Exception as e:
        sock.close()
        raise ConnectionError(f"Error inesperado conectando a {host}:{puerto}: {e}")


def es_puerto_abierto(host: str, puerto: int, timeout: float = 1.0) -> bool:
    """Verificación rápida si un puerto está abierto (sin mantener conexión).

    Args:
        host: Host objetivo.
        puerto: Puerto a verificar.
        timeout: Tiempo máximo de espera.

    Returns:
        True si el puerto aceptó la conexión, False en caso contrario.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        resultado = sock.connect_ex((host, puerto))
        return resultado == 0
