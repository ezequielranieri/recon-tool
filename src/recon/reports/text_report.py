"""Módulo para exportar resultados de escaneo a formato de texto legible."""

from pathlib import Path

from recon.core.models import ResultadoEscaneo


def generar_reporte_texto(resultado: ResultadoEscaneo, path: Path) -> None:
    """Exporta el resultado del escaneo a un archivo de texto legible.

    Args:
        resultado: Objeto ResultadoEscaneo con la información capturada.
        path: Ruta del archivo donde se guardará el reporte.
    """
    lineas = [
        "========================================",
        "      REPORTE DE ESCANEO DE RED",
        "========================================",
        f"Host:      {resultado.host}",
        f"IP:        {resultado.ip}",
        f"Fecha:     {resultado.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Duración:  {resultado.duracion_segundos:.2f}s",
        f"Puertos:   {resultado.puertos_escaneados} escaneados",
        "----------------------------------------",
        f"Puertos abiertos encontrados: {len(resultado.puertos_abiertos)}",
        "----------------------------------------",
    ]

    if resultado.puertos_abiertos:
        lineas.append(f"{'PUERTO':<8} {'ESTADO':<10} {'SERVICIO':<15} {'BANNER'}")
        lineas.append("-" * 60)
        for p in resultado.puertos_abiertos:
            servicio = p.servicio or "desconocido"
            banner = p.banner or "-"
            lineas.append(f"{p.puerto:<8} {p.estado:<10} {servicio:<15} {banner}")
    else:
        lineas.append("No se detectaron puertos abiertos.")

    lineas.append("----------------------------------------")
    lineas.append("Fin del reporte.")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))
