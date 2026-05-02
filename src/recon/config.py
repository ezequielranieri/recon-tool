"""Configuración centralizada del proyecto usando Pydantic Settings."""

import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación.

    Atributos:
        app_name: Nombre de la herramienta.
        debug: Modo depuración activo o no.
        timeout_default: Tiempo de espera por defecto para escaneos.
        max_workers: Número máximo de trabajadores concurrentes.
        log_level: Nivel de logging.
    """

    app_name: str = "recon-tool"
    debug: bool = False
    timeout_default: float = 1.0
    max_workers: int = 100
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

# Configuración básica de logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("recon")
