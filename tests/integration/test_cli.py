"""Pruebas de integración para la interfaz CLI."""

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from recon.cli import app
from recon.core.models import ResultadoPuerto

runner = CliRunner()


@pytest.fixture
def mock_scan_results():
    """Simula resultados de escaneo para evitar conexiones reales."""
    return [
        ResultadoPuerto(
            puerto=80, estado="abierto", servicio="HTTP", banner="nginx", tiempo_ms=10.0
        ),
        ResultadoPuerto(
            puerto=443,
            estado="abierto",
            servicio="HTTPS",
            banner=None,
            tiempo_ms=12.0,
        ),
    ]


def test_cli_scan_help():
    """Verifica que el comando de ayuda funcione."""
    result = runner.invoke(app, ["scan", "--help"])
    assert result.exit_code == 0
    assert "Escanea un host en busca de puertos abiertos y servicios" in result.stdout


@patch("recon.cli.validar_host")
@patch("recon.cli.parsear_puertos")
@patch("recon.cli.asyncio.run")
def test_cli_scan_success(mock_async_run, mock_parse_puertos, mock_validar_host):
    """Prueba un escaneo exitoso (con mocks)."""
    # Configurar mocks
    mock_validar_host.return_value = "8.8.8.8"
    mock_parse_puertos.return_value = [80, 443]

    # Mock del resultado del escaneo
    mock_resultado = MagicMock()
    mock_resultado.puertos_abiertos = [
        ResultadoPuerto(
            puerto=80, estado="abierto", servicio="HTTP", banner="nginx", tiempo_ms=1.0
        )
    ]
    mock_resultado.duracion_segundos = 1.5
    mock_resultado.puertos_escaneados = 2
    mock_async_run.return_value = mock_resultado

    result = runner.invoke(app, ["scan", "8.8.8.8", "--ports", "80,443"])

    assert result.exit_code == 0
    assert "Target:  8.8.8.8" in result.stdout
    assert "80" in result.stdout
    assert "abierto" in result.stdout
    assert "HTTP" in result.stdout


def test_cli_scan_invalid_host():
    """Verifica el manejo de error ante un host inválido."""
    result = runner.invoke(app, ["scan", "invalid_host!!!"])
    assert result.exit_code == 1
    assert "Error de validación" in result.stdout


@patch("recon.cli.validar_host")
@patch("recon.cli.parsear_puertos")
@patch("recon.cli.asyncio.run")
def test_cli_scan_with_report(
    mock_async_run, mock_parse_puertos, mock_validar_host, tmp_path
):
    """Prueba la generación de reporte desde la CLI."""
    mock_validar_host.return_value = "8.8.8.8"
    mock_parse_puertos.return_value = [80]

    mock_resultado = MagicMock()
    mock_resultado.puertos_abiertos = []
    mock_resultado.duracion_segundos = 0.5
    mock_resultado.puertos_escaneados = 1
    mock_async_run.return_value = mock_resultado

    report_file = tmp_path / "report.txt"
    result = runner.invoke(app, ["scan", "8.8.8.8", "--output", str(report_file)])

    assert result.exit_code == 0
    assert "Reporte en" in result.stdout
    assert report_file.exists()
