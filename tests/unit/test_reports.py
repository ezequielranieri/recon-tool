"""Pruebas unitarias para los módulos de reporte."""

import json
from datetime import datetime

import pytest

from recon.core.models import ResultadoEscaneo, ResultadoPuerto
from recon.reports.json_report import generar_reporte_json
from recon.reports.text_report import generar_reporte_texto


@pytest.fixture
def resultado_mock():
    """Crea un objeto ResultadoEscaneo para pruebas."""
    return ResultadoEscaneo(
        host="example.com",
        ip="93.184.216.34",
        timestamp=datetime(2026, 5, 2, 12, 0, 0),
        duracion_segundos=2.5,
        puertos_escaneados=10,
        puertos_abiertos=[
            ResultadoPuerto(
                puerto=80,
                estado="abierto",
                servicio="HTTP",
                banner="nginx/1.24.0",
                tiempo_ms=10.5,
            ),
            ResultadoPuerto(
                puerto=443,
                estado="abierto",
                servicio="HTTPS",
                banner=None,
                tiempo_ms=12.1,
            ),
        ],
    )


def test_generar_reporte_json(resultado_mock, tmp_path):
    """Verifica que el reporte JSON se genere correctamente."""
    archivo = tmp_path / "reporte.json"
    generar_reporte_json(resultado_mock, archivo)

    assert archivo.exists()

    with open(archivo, encoding="utf-8") as f:
        datos = json.load(f)

    assert datos["host"] == "example.com"
    assert datos["ip"] == "93.184.216.34"
    assert len(datos["puertos_abiertos"]) == 2
    assert datos["puertos_abiertos"][0]["puerto"] == 80


def test_generar_reporte_texto(resultado_mock, tmp_path):
    """Verifica que el reporte de texto se genere correctamente."""
    archivo = tmp_path / "reporte.txt"
    generar_reporte_texto(resultado_mock, archivo)

    assert archivo.exists()

    contenido = archivo.read_text(encoding="utf-8")
    assert "Host:      example.com" in contenido
    assert "93.184.216.34" in contenido
    assert "80" in contenido
    assert "nginx/1.24.0" in contenido
    assert "443" in contenido
    assert "HTTPS" in contenido
