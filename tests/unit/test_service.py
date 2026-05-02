"""Unit tests for the service identification module."""

from recon.core.service import identificar_servicio


def test_identificar_por_puerto_estandar():
    """Verifies identification by known port."""
    assert identificar_servicio(80) == "HTTP"
    assert identificar_servicio(22) == "SSH"
    assert identificar_servicio(443) == "HTTPS"


def test_identificar_por_banner_puerto_no_estandar():
    """Verifies that the banner has priority over unknown ports."""
    # Random port, but SSH banner
    assert identificar_servicio(12345, banner="SSH-2.0-OpenSSH_8.9") == "SSH"
    # Random port, HTTP banner
    assert identificar_servicio(8081, banner="HTTP/1.1 200 OK") == "HTTP"


def test_servicio_desconocido():
    """Verifies return for unmapped services and without banner."""
    assert identificar_servicio(9999) == "unknown"


def test_identificar_por_banner_heuristica():
    """Tests banner heuristics."""
    banner_mysql = "5.7.44-0ubuntu0.18.04.1-log MySQL Community Server"
    assert identificar_servicio(3306, banner=banner_mysql) == "MySQL"
    assert identificar_servicio(6379, banner="Redis server v=6.0.16") == "Redis"
    # HTTP with specific headers
    assert identificar_servicio(8081, banner="Server: Apache/2.4.41") == "HTTP"
    assert identificar_servicio(8081, banner="HTTP/1.1 200 OK") == "HTTP"
    # Should not give false positives with generic HTML tags if no headers
    assert identificar_servicio(8081, banner="<HTML><BODY>Hello</BODY></HTML>") == "unknown"
