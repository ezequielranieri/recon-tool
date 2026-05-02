"""Pruebas unitarias para el módulo de validación."""

import pytest

from recon.utils.validators import parsear_puertos, validar_host, validar_puerto


class TestValidators:
    """Suite de pruebas para validaciones de seguridad y formato."""

    def test_validar_host_ip_publica(self):
        """IPs públicas válidas deben ser aceptadas."""
        assert validar_host("8.8.8.8") == "8.8.8.8"
        assert validar_host("1.1.1.1") == "1.1.1.1"

    def test_validar_host_ip_reservada(self):
        """IPs reservadas/locales deben ser rechazadas por seguridad."""
        with pytest.raises(ValueError, match="está reservada"):
            validar_host("127.0.0.1")
        with pytest.raises(ValueError, match="está reservada"):
            validar_host("0.0.0.0")

    def test_validar_host_hostname_valido(self):
        """Hostnames válidos deben ser aceptados."""
        assert validar_host("google.com") == "google.com"
        assert validar_host("mi-servidor.local.com") == "mi-servidor.local.com"

    def test_validar_host_invalido(self):
        """Hostnames con caracteres prohibidos deben ser rechazados."""
        with pytest.raises(ValueError, match="Hostname inválido"):
            validar_host("host_invalido")
        with pytest.raises(ValueError, match="Hostname inválido"):
            validar_host("google.com; drop table users")

    def test_validar_puerto_rango(self):
        """Puertos deben estar entre 1 y 65535."""
        assert validar_puerto(80) == 80
        assert validar_puerto(65535) == 65535
        with pytest.raises(ValueError, match="fuera de rango"):
            validar_puerto(0)
        with pytest.raises(ValueError, match="fuera de rango"):
            validar_puerto(65536)

    def test_parsear_puertos_lista(self):
        """Parsea correctamente lista separada por comas."""
        assert parsear_puertos("80, 443, 8080") == [80, 443, 8080]

    def test_parsear_puertos_rango(self):
        """Parsea correctamente rangos."""
        assert parsear_puertos("1-5") == [1, 2, 3, 4, 5]

    def test_parsear_puertos_mixto(self):
        """Parsea correctamente formatos mixtos y elimina duplicados."""
        assert parsear_puertos("22, 80-82, 22") == [22, 80, 81, 82]

    def test_parsear_puertos_invalido(self):
        """Rechaza formatos de puerto malformados."""
        with pytest.raises(ValueError):
            parsear_puertos("abc")
        with pytest.raises(ValueError):
            parsear_puertos("80-70")  # Rango invertido
        with pytest.raises(ValueError):
            parsear_puertos("1-70000")  # Fuera de rango
