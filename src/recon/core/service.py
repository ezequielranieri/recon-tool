"""Módulo para la identificación de servicios basados en puertos y banners."""

# Mapeo mínimo obligatorio según proyecto_recon.md
SERVICIOS_CONOCIDOS: dict[int, str] = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017: "MongoDB",
}


def identificar_servicio(puerto: int, banner: str | None = None) -> str:
    """Identifica el servicio asociado a un puerto.

    Prioriza la detección por banner si el puerto no es estándar,
    o confirma el servicio si el banner coincide con el puerto.

    Args:
        puerto: Puerto escaneado.
        banner: Banner capturado (opcional).

    Returns:
        Nombre del servicio identificado o "desconocido".
    """
    # 1. Intentar identificar por banner (heurística básica)
    if banner:
        banner_upper = banner.upper()
        if "SSH" in banner_upper:
            return "SSH"
        if "HTTP" in banner_upper or "HTML" in banner_upper:
            return "HTTP"
        if "FTP" in banner_upper:
            return "FTP"
        if "MYSQL" in banner_upper:
            return "MySQL"
        if "POSTGRES" in banner_upper:
            return "PostgreSQL"
        if "REDIS" in banner_upper:
            return "Redis"

    # 2. Si no hay banner o no hubo match, usar mapeo por puerto
    return SERVICIOS_CONOCIDOS.get(puerto, "desconocido")
