"""Pruebas unitarias para el módulo de escaneo."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from recon.core.models import ResultadoPuerto
from recon.core.scanner import escanear_puerto, escanear_rango


class TestScanner:
    """Suite de pruebas para el escáner de puertos."""

    @pytest.mark.asyncio
    async def test_escanear_puerto_abierto(self):
        """Verifica que un puerto abierto se detecte correctamente."""
        # Mock de asyncio.open_connection para simular éxito
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
            assert resultado.estado == "abierto"
            assert resultado.tiempo_ms >= 0

    @pytest.mark.asyncio
    async def test_escanear_puerto_cerrado(self):
        """Verifica que un puerto cerrado (conexión rechazada) se detecte."""
        with patch(
            "asyncio.open_connection", AsyncMock(side_effect=ConnectionRefusedError())
        ):
            resultado = await escanear_puerto("127.0.0.1", 81, timeout=0.1)

            assert resultado.estado == "cerrado"

    @pytest.mark.asyncio
    async def test_escanear_puerto_filtrado(self):
        """Verifica que un timeout se interprete como puerto filtrado."""
        with patch("asyncio.open_connection", AsyncMock(side_effect=TimeoutError())):
            resultado = await escanear_puerto("127.0.0.1", 443, timeout=0.1)

            assert resultado.estado == "filtrado"

    @pytest.mark.asyncio
    async def test_escanear_rango_concurrente(self):
        """Verifica que el escaneo de rango funcione y sea concurrente."""
        puertos = [80, 443, 8080]

        # Simulamos que todos están cerrados para simplificar
        with patch(
            "asyncio.open_connection", AsyncMock(side_effect=ConnectionRefusedError())
        ):
            resultados = await escanear_rango("127.0.0.1", puertos, max_workers=2)

            assert len(resultados) == 3
            for r in resultados:
                assert r.puerto in puertos
                assert r.estado == "cerrado"

    @pytest.mark.asyncio
    async def test_validacion_rango_puertos(self):
        """Pydantic debe validar que el puerto esté entre 1 y 65535."""
        with pytest.raises(ValueError):
            ResultadoPuerto(puerto=70000, estado="abierto", tiempo_ms=1.0)

        with pytest.raises(ValueError):
            ResultadoPuerto(puerto=0, estado="abierto", tiempo_ms=1.0)
