"""Módulo para exportar resultados de escaneo a formato JSON."""

from pathlib import Path

from recon.core.models import ResultadoEscaneo


def generar_reporte_json(resultado: ResultadoEscaneo, path: Path) -> None:
    """Exporta el resultado del escaneo a un archivo JSON.

    Args:
        resultado: Objeto ResultadoEscaneo con la información capturada.
        path: Ruta del archivo donde se guardará el reporte.
    """
    # Usamos model_dump_json para serializar correctamente objetos como datetime
    datos_json = resultado.model_dump_json(indent=4)

    with open(path, "w", encoding="utf-8") as f:
        f.write(datos_json)
