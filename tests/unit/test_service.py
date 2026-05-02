"""Pruebas unitarias para el módulo de identificación de servicios."""

from recon.core.service import identificar_servicio


def test_identificar_por_puerto_estandar():
    """Verifica identificación por puerto conocido."""
    assert identificar_servicio(80) == "HTTP"
    assert identificar_servicio(22) == "SSH"
    assert identificar_servicio(443) == "HTTPS"


def test_identificar_por_banner_puerto_no_estandar():
    """Verifica que el banner tiene prioridad sobre puertos desconocidos."""
    # Puerto random, pero banner de SSH
    assert identificar_servicio(12345, banner="SSH-2.0-OpenSSH_8.9") == "SSH"
    # Puerto random, banner de HTTP
    assert identificar_servicio(8081, banner="HTTP/1.1 200 OK") == "HTTP"


def test_servicio_desconocido():
    """Verifica retorno para servicios no mapeados y sin banner."""
    assert identificar_servicio(9999) == "desconocido"


def test_identificar_por_banner_heuristica():
    """Prueba las heurísticas de banners."""
    banner_mysql = "5.7.44-0ubuntu0.18.04.1-log MySQL Community Server"
    assert identificar_servicio(3306, banner=banner_mysql) == "MySQL"
    assert identificar_servicio(6379, banner="Redis server v=6.0.16") == "Redis"
