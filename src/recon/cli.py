"""Interfaz de línea de comandos (CLI) profesional para recon-tool."""

import asyncio
import time
from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Table

from recon.config import logger, settings
from recon.core.banner import capturar_banner
from recon.core.models import ResultadoEscaneo, ResultadoPuerto
from recon.core.scanner import escanear_puerto
from recon.core.service import identificar_servicio
from recon.reports.json_report import generar_reporte_json
from recon.reports.text_report import generar_reporte_texto
from recon.utils.validators import parsear_puertos, validar_host


class FormatoReporte(StrEnum):
    """Formatos de reporte soportados."""

    JSON = "json"
    TEXT = "text"


app = typer.Typer(
    help=f"🚀 {settings.app_name} - Professional Network Reconnaissance Tool",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()


async def ejecutar_escaneo(
    host: str,
    puertos: list[int],
    timeout: float,
    workers: int,
) -> ResultadoEscaneo:
    """Orquestra el escaneo asíncrono con barra de progreso."""
    semaforo = asyncio.Semaphore(workers)
    puertos_abiertos: list[ResultadoPuerto] = []
    start_time = time.monotonic()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(f"[cyan]Escaneando {host}...", total=len(puertos))

        async def scan_task(p: int) -> None:
            res = await escanear_puerto(host, p, timeout, semaforo)
            if res.estado == "abierto":
                res.banner = await capturar_banner(host, p, timeout=timeout)
                res.servicio = identificar_servicio(p, res.banner)
                puertos_abiertos.append(res)
            progress.update(task, advance=1)

        await asyncio.gather(*(scan_task(p) for p in puertos))

    return ResultadoEscaneo(
        host=host,
        ip=host,
        duracion_segundos=time.monotonic() - start_time,
        puertos_escaneados=len(puertos),
        puertos_abiertos=sorted(puertos_abiertos, key=lambda x: x.puerto),
    )


@app.command(name="scan")
def scan(
    host: Annotated[str, typer.Argument(help="Host o IP objetivo a escanear")],
    ports: Annotated[
        str, typer.Option("--ports", "-p", help="Puertos (ej: 80,443 o 1-1024)")
    ] = "1-1000",
    timeout: Annotated[
        float, typer.Option("--timeout", "-t", help="Timeout por puerto (s)")
    ] = settings.timeout_default,
    workers: Annotated[
        int, typer.Option("--workers", "-w", help="Escaneos concurrentes")
    ] = settings.max_workers,
    output: Annotated[
        Path | None, typer.Option("--output", "-o", help="Ruta de reporte")
    ] = None,
    format_rep: Annotated[
        FormatoReporte, typer.Option("--format", "-f", help="Formato del reporte")
    ] = FormatoReporte.TEXT,
) -> None:
    """Escanea un host en busca de puertos abiertos y servicios."""
    console.print(
        Panel.fit(
            f"[bold blue]{settings.app_name}[/bold blue] v0.1.0\n"
            f"[dim]Network Reconnaissance Tool[/dim]",
            border_style="blue",
        )
    )

    try:
        host_v = validar_host(host)
        lista_p = parsear_puertos(ports)

        console.print(f"[bold]Target:[/bold]  [green]{host_v}[/green]")
        console.print(
            f"[bold]Puertos:[/bold] [yellow]{ports}[/yellow] ({len(lista_p)})"
        )
        console.print(f"[bold]Workers:[/bold] [cyan]{workers}[/cyan] | {timeout}s")
        console.print("")

        res = asyncio.run(ejecutar_escaneo(host_v, lista_p, timeout, workers))

        if res.puertos_abiertos:
            table = Table(
                title=f"Resultados para {host_v}",
                show_header=True,
                header_style="bold magenta",
            )
            table.add_column("Puerto", style="dim", width=8)
            table.add_column("Estado", justify="center")
            table.add_column("Servicio", style="cyan")
            table.add_column("Banner", style="green")

            for p in res.puertos_abiertos:
                table.add_row(
                    str(p.puerto),
                    "[bold green]abierto[/bold green]",
                    p.servicio or "desconocido",
                    p.banner or "-",
                )
            console.print(table)
        else:
            console.print("\n[yellow]No se encontraron puertos abiertos.[/yellow]")

        console.print(f"\n[bold blue]Completado en {res.duracion_segundos:.2f}s[/]")
        console.print(f"Abiertos: [bold green]{len(res.puertos_abiertos)}[/]")

        if output:
            if format_rep == FormatoReporte.JSON:
                generar_reporte_json(res, output)
            else:
                generar_reporte_texto(res, output)
            console.print(
                f"\n[bold green]✅ Reporte en:[/bold green] [underline]{output}[/]"
            )

    except ValueError as e:
        console.print(f"\n[bold red]❌ Error de validación:[/bold red] {e}")
        raise typer.Exit(code=1) from e
    except Exception as e:
        logger.exception("Error inesperado en el CLI")
        console.print(f"\n[bold red]❌ Error inesperado:[/bold red] {e}")
        raise typer.Exit(code=1) from e


@app.callback()
def main() -> None:
    """Herramienta profesional de reconocimiento de red."""
    pass


if __name__ == "__main__":
    app()
