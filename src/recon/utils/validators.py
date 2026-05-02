"""Validation module for hosts and ports with a security focus."""

import re
from ipaddress import AddressValueError, ip_address, ip_network

# Reserved networks according to seguridad.md
REDES_RESERVADAS = [
    ip_network("0.0.0.0/8"),
    ip_network("10.0.0.0/8"),
    ip_network("127.0.0.0/8"),
    ip_network("169.254.0.0/16"),
    ip_network("172.16.0.0/12"),
    ip_network("192.168.0.0/16"),
    ip_network("224.0.0.0/4"),
    ip_network("240.0.0.0/4"),
]

PUERTO_MIN = 1
PUERTO_MAX = 65535


def validar_host(host: str) -> str:
    """Validates that the host is a valid IP or a secure hostname.

    Args:
        host: Hostname or IP to validate.

    Returns:
        The validated host.

    Raises:
        ValueError: If the host is invalid or a reserved IP.
    """
    # 1. Try as IP
    es_ip = False
    try:
        addr = ip_address(host)
        es_ip = True
        # Check if it is a reserved IP
        if any(addr in red for red in REDES_RESERVADAS):
            raise ValueError(
                f"The IP address {host} is reserved and not scannable"
            )
        return str(addr)

    except (ValueError, AddressValueError):
        # If it was an IP and threw ValueError for being reserved, re-throw
        if es_ip:
            raise
        pass

    # 2. Validate as hostname (RFC 1123)
    patron = re.compile(
        r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$"
    )
    if not patron.match(host) and host != "localhost":
        raise ValueError(f"Invalid hostname: {host}")

    return host


def validar_puerto(puerto: int) -> int:
    """Validates that the port is within the allowed range.

    Args:
        puerto: Port number.

    Returns:
        The port if valid.

    Raises:
        ValueError: If the port is out of range.
    """
    if not PUERTO_MIN <= puerto <= PUERTO_MAX:
        raise ValueError(
            f"Port {puerto} out of valid range ({PUERTO_MIN}-{PUERTO_MAX})"
        )
    return puerto


def parsear_puertos(input_puertos: str) -> list[int]:
    """Parses a port string (e.g.: '80,443', '1-1024').

    Args:
        input_puertos: String with port specification.

    Returns:
        List of unique and sorted ports.

    Raises:
        ValueError: If the format is invalid or any port is out of range.
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
                    raise ValueError(f"Invalid range: {parte}")
                for p in range(inicio, fin + 1):
                    puertos.add(validar_puerto(p))
            except ValueError as e:
                if "Invalid range" in str(e) or "Port" in str(e):
                    raise
                raise ValueError(f"Invalid range format: {parte}") from e
        else:
            try:
                puerto = int(parte)
                puertos.add(validar_puerto(puerto))
            except ValueError as e:
                if "Port" in str(e):
                    raise
                raise ValueError(f"Invalid port number: {parte}") from e

    if not puertos:
        raise ValueError("No valid ports specified")

    return sorted(list(puertos))
