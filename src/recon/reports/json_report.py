"""Module for exporting scan results to JSON format."""

from pathlib import Path

from recon.core.models import ResultadoEscaneo


def generar_reporte_json(resultado: ResultadoEscaneo, path: Path) -> None:
    """Exports the scan result to a JSON file.

    Args:
        resultado: ResultadoEscaneo object with the captured information.
        path: Path to the file where the report will be saved.
    """
    # We use model_dump_json to correctly serialize objects like datetime
    datos_json = resultado.model_dump_json(indent=4)

    with open(path, "w", encoding="utf-8") as f:
        f.write(datos_json)
