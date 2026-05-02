"""Module for exporting scan results to human-readable text format."""

from pathlib import Path

from recon.core.models import ResultadoEscaneo


def generar_reporte_texto(resultado: ResultadoEscaneo, path: Path) -> None:
    """Exports the scan result to a human-readable text file.

    Args:
        resultado: ResultadoEscaneo object with the captured information.
        path: Path to the file where the report will be saved.
    """
    lineas = [
        "========================================",
        "          NETWORK SCAN REPORT",
        "========================================",
        f"Host:      {resultado.host}",
        f"IP:        {resultado.ip}",
        f"Date:      {resultado.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Duration:  {resultado.duracion_segundos:.2f}s",
        f"Ports:     {resultado.puertos_escaneados} scanned",
        "----------------------------------------",
        f"Open ports found: {len(resultado.puertos_abiertos)}",
        "----------------------------------------",
    ]

    if resultado.puertos_abiertos:
        lineas.append(f"{'PORT':<8} {'STATE':<10} {'SERVICE':<15} {'BANNER'}")
        lineas.append("-" * 60)
        for p in resultado.puertos_abiertos:
            servicio = p.servicio or "unknown"
            banner = p.banner or "-"
            lineas.append(f"{p.puerto:<8} {p.estado:<10} {servicio:<15} {banner}")
    else:
        lineas.append("No open ports detected.")

    lineas.append("----------------------------------------")
    lineas.append("End of report.")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))
