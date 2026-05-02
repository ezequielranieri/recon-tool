"""Module for service identification based on ports and banners."""

# Minimum mandatory mapping according to proyecto_recon.md
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
    """Identifies the service associated with a port.

    Prioritizes banner detection if the port is non-standard,
    or confirms the service if the banner matches the port.

    Args:
        puerto: Scanned port.
        banner: Captured banner (optional).

    Returns:
        Name of the identified service or "unknown".
    """
    # 1. Attempt to identify by banner (basic heuristic)
    if banner:
        banner_upper = banner.upper()
        if "SSH" in banner_upper:
            return "SSH"
        # Refined heuristic for HTTP
        if any(mark in banner_upper for mark in ["HTTP/1.", "HTTP/1.1", "HTTP/2", "SERVER:", "CONTENT-TYPE:"]):
            return "HTTP"
        if "FTP" in banner_upper:
            return "FTP"
        if "MYSQL" in banner_upper:
            return "MySQL"
        if "POSTGRES" in banner_upper:
            return "PostgreSQL"
        if "REDIS" in banner_upper:
            return "Redis"

    # 2. If no banner or no match, use port mapping
    return SERVICIOS_CONOCIDOS.get(puerto, "unknown")
