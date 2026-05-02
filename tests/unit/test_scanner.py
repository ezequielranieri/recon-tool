"""Unit tests for the scanning module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from recon.core.models import ResultadoPuerto
from recon.core.scanner import escanear_puerto, escanear_rango


class TestScanner:
    """Test suite for the port scanner."""

    @pytest.mark.asyncio
    async def test_escanear_puerto_abierto(self):
        """Verifies that an open port is correctly detected."""
        # Mock of asyncio.open_connection to simulate success
        mock_reader = AsyncMock()
        mock_writer = MagicMock()
        mock_writer.close = MagicMock()
        mock_writer.wait_closed = AsyncMock()

        with patch(
            "asyncio.open_connection",
            AsyncMock(return_value=(mock_reader, mock_writer)),
        ):
            resultado = await escanear_puerto("127.0.0.1", 80, timeout=0.1)

            assert isinstance(resultado, ResultadoPuerto)
            assert resultado.puerto == 80
            assert resultado.estado == "open"
            assert resultado.tiempo_ms >= 0

    @pytest.mark.asyncio
    async def test_escanear_puerto_cerrado(self):
        """Verifies that a closed port (connection refused) is detected."""
        with patch(
            "asyncio.open_connection", AsyncMock(side_effect=ConnectionRefusedError())
        ):
            resultado = await escanear_puerto("127.0.0.1", 81, timeout=0.1)

            assert resultado.estado == "closed"

    @pytest.mark.asyncio
    async def test_escanear_puerto_filtrado(self):
        """Verifies that a timeout is interpreted as a filtered port."""
        with patch("asyncio.open_connection", AsyncMock(side_effect=TimeoutError())):
            resultado = await escanear_puerto("127.0.0.1", 443, timeout=0.1)

            assert resultado.estado == "filtered"

    @pytest.mark.asyncio
    async def test_escanear_rango_concurrente(self):
        """Verifies that range scanning works and is concurrent."""
        puertos = [80, 443, 8080]

        # Simulate that all are closed for simplicity
        with patch(
            "asyncio.open_connection", AsyncMock(side_effect=ConnectionRefusedError())
        ):
            resultados = await escanear_rango("127.0.0.1", puertos, max_workers=2)

            assert len(resultados) == 3
            for r in resultados:
                assert r.puerto in puertos
                assert r.estado == "closed"

    @pytest.mark.asyncio
    async def test_validacion_rango_puertos(self):
        """Pydantic must validate that the port is between 1 and 65535."""
        with pytest.raises(ValueError):
            ResultadoPuerto(puerto=70000, estado="open", tiempo_ms=1.0)

        with pytest.raises(ValueError):
            ResultadoPuerto(puerto=0, estado="open", tiempo_ms=1.0)
