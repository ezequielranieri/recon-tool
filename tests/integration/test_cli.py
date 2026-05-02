"""Integration tests for the CLI interface."""

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from recon.cli import app
from recon.core.models import ResultadoPuerto

runner = CliRunner()


@pytest.fixture
def mock_scan_results():
    """Simulates scan results to avoid real connections."""
    return [
        ResultadoPuerto(
            puerto=80, estado="open", servicio="HTTP", banner="nginx", tiempo_ms=10.0
        ),
        ResultadoPuerto(
            puerto=443,
            estado="open",
            servicio="HTTPS",
            banner=None,
            tiempo_ms=12.0,
        ),
    ]


def test_cli_scan_help():
    """Verifies that the help command works."""
    result = runner.invoke(app, ["scan", "--help"])
    assert result.exit_code == 0
    assert "Scan a host for open ports and services" in result.stdout


@patch("recon.cli.validar_host")
@patch("recon.cli.parsear_puertos")
@patch("recon.cli.ejecutar_escaneo")
def test_cli_scan_success(mock_ejecutar_escaneo, mock_parse_puertos, mock_validar_host):
    """Tests a successful scan (with mocks)."""
    # Configure mocks
    mock_validar_host.return_value = "8.8.8.8"
    mock_parse_puertos.return_value = [80, 443]

    # Mock of the scan result
    mock_resultado = MagicMock()
    mock_resultado.puertos_abiertos = [
        ResultadoPuerto(
            puerto=80, estado="open", servicio="HTTP", banner="nginx", tiempo_ms=1.0
        )
    ]
    mock_resultado.duracion_segundos = 1.5
    mock_resultado.puertos_escaneados = 2
    mock_ejecutar_escaneo.return_value = mock_resultado

    result = runner.invoke(app, ["scan", "8.8.8.8", "--ports", "80,443"])

    assert result.exit_code == 0
    assert "Target:  8.8.8.8" in result.stdout
    assert "80" in result.stdout
    assert "open" in result.stdout
    assert "HTTP" in result.stdout


def test_cli_scan_invalid_host():
    """Verifies error handling for an invalid host."""
    result = runner.invoke(app, ["scan", "invalid_host!!!"])
    assert result.exit_code == 1
    assert "Validation Error" in result.stdout


@patch("recon.cli.validar_host")
@patch("recon.cli.parsear_puertos")
@patch("recon.cli.ejecutar_escaneo")
def test_cli_scan_with_report(
    mock_ejecutar_escaneo, mock_parse_puertos, mock_validar_host, tmp_path
):
    """Tests report generation from the CLI."""
    mock_validar_host.return_value = "8.8.8.8"
    mock_parse_puertos.return_value = [80]

    mock_resultado = MagicMock()
    mock_resultado.puertos_abiertos = []
    mock_resultado.duracion_segundos = 0.5
    mock_resultado.puertos_escaneados = 1
    mock_ejecutar_escaneo.return_value = mock_resultado

    report_file = tmp_path / "report.txt"
    result = runner.invoke(app, ["scan", "8.8.8.8", "--output", str(report_file)])

    assert result.exit_code == 0
    assert "Report saved at" in result.stdout
    assert report_file.exists()
