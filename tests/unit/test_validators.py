"""Unit tests for the validation module."""

import pytest

from recon.utils.validators import parsear_puertos, validar_host, validar_puerto


class TestValidators:
    """Test suite for security and format validations."""

    def test_validar_host_ip_publica(self):
        """Valid public IPs must be accepted."""
        assert validar_host("8.8.8.8") == "8.8.8.8"
        assert validar_host("1.1.1.1") == "1.1.1.1"

    def test_validar_host_ip_reservada(self):
        """Reserved/local IPs must be rejected for security."""
        with pytest.raises(ValueError, match="is reserved"):
            validar_host("127.0.0.1")
        with pytest.raises(ValueError, match="is reserved"):
            validar_host("0.0.0.0")

    def test_validar_host_hostname_valido(self):
        """Valid hostnames must be accepted."""
        assert validar_host("google.com") == "google.com"
        assert validar_host("my-server.local.com") == "my-server.local.com"

    def test_validar_host_invalido(self):
        """Hostnames with forbidden characters must be rejected."""
        with pytest.raises(ValueError, match="Invalid hostname"):
            validar_host("invalid_host")
        with pytest.raises(ValueError, match="Invalid hostname"):
            validar_host("google.com; drop table users")

    def test_validar_puerto_rango(self):
        """Ports must be between 1 and 65535."""
        assert validar_puerto(80) == 80
        assert validar_puerto(65535) == 65535
        with pytest.raises(ValueError, match="out of valid range"):
            validar_puerto(0)
        with pytest.raises(ValueError, match="out of valid range"):
            validar_puerto(65536)

    def test_parsear_puertos_lista(self):
        """Correctly parses comma-separated list."""
        assert parsear_puertos("80, 443, 8080") == [80, 443, 8080]

    def test_parsear_puertos_rango(self):
        """Correctly parses ranges."""
        assert parsear_puertos("1-5") == [1, 2, 3, 4, 5]

    def test_parsear_puertos_mixto(self):
        """Correctly parses mixed formats and removes duplicates."""
        assert parsear_puertos("22, 80-82, 22") == [22, 80, 81, 82]

    def test_parsear_puertos_invalido(self):
        """Rejects malformed port formats."""
        with pytest.raises(ValueError):
            parsear_puertos("abc")
        with pytest.raises(ValueError, match="Invalid range"):
            parsear_puertos("80-70")  # Inverted range
        with pytest.raises(ValueError, match="out of valid range"):
            parsear_puertos("1-70000")  # Out of range
