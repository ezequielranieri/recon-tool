"""Módulo de validación para hosts y puertos con enfoque en seguridad."""

import re
from ipaddress import AddressValueError, ip_address, ip_network

# Redes reservadas según seguridad.md
REDES_RESERVADAS = [
    ip_network("0.0.0.0/8"),
    ip_network("127.0.0.0/8"),
    ip_network("169.254.0.0/16"),
    ip_network("224.0.0.0/4"),
    ip_network("240.0.0.0/4"),
]

PUERTO_MIN = 1
PUERTO_MAX = 65535


def validar_host(host: str) -> str:
    """Valida que el host sea una IP válida o un hostname seguro.

    Args:
        host: Hostname o IP a validar.

    Returns:
        El host validado.

    Raises:
        ValueError: Si el host no es válido o es una IP reservada.
    """
    # 1. Intentar como IP
    es_ip = False
    try:
        addr = ip_address(host)
        es_ip = True
        # Verificar si es una IP reservada
        if any(addr in red for red in REDES_RESERVADAS):
            raise ValueError(
                f"La dirección IP {host} está reservada y no es escaneable"
            )
        return str(addr)

    except (ValueError, AddressValueError):
        # Si era una IP y lanzó ValueError por estar reservada, re-lanzar
        if es_ip:
            raise
        pass

    # 2. Validar como hostname (RFC 1123)
    patron = re.compile(
        r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$"
    )
    if not patron.match(host) and host != "localhost":
        raise ValueError(f"Hostname inválido: {host}")

    return host


def validar_puerto(puerto: int) -> int:
    """Valida que el puerto esté en el rango permitido.

    Args:
        puerto: Número de puerto.

    Returns:
        El puerto si es válido.

    Raises:
        ValueError: Si el puerto está fuera de rango.
    """
    if not PUERTO_MIN <= puerto <= PUERTO_MAX:
        raise ValueError(
            f"Puerto {puerto} fuera de rango válido ({PUERTO_MIN}-{PUERTO_MAX})"
        )
    return puerto


def parsear_puertos(input_puertos: str) -> list[int]:
    """Parsea una cadena de puertos (ej: '80,443', '1-1024').

    Args:
        input_puertos: String con la especificación de puertos.

    Returns:
        Lista de puertos únicos y ordenados.

    Raises:
        ValueError: Si el formato es inválido o algún puerto está fuera de rango.
    """
    puertos: set[int] = set()
    partes = input_puertos.split(",")

    for parte in partes:
        parte = parte.strip()
        if "-" in parte:
            try:
                inicio_str, fin_str = parte.split("-")
                inicio = int(inicio_str)
                fin = int(fin_str)
                if inicio > fin:
                    raise ValueError(f"Rango inválido: {parte}")
                for p in range(inicio, fin + 1):
                    puertos.add(validar_puerto(p))
            except ValueError as e:
                if "Rango inválido" in str(e) or "Puerto" in str(e):
                    raise
                raise ValueError(f"Formato de rango inválido: {parte}") from e
        else:
            try:
                puerto = int(parte)
                puertos.add(validar_puerto(puerto))
            except ValueError as e:
                if "Puerto" in str(e):
                    raise
                raise ValueError(f"Número de puerto inválido: {parte}") from e

    if not puertos:
        raise ValueError("No se especificaron puertos válidos")

    return sorted(list(puertos))
