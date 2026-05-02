"""Centralized project configuration using Pydantic Settings."""

import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration.

    Attributes:
        app_name: Tool name.
        debug: Debug mode active or not.
        timeout_default: Default timeout for scans.
        max_workers: Maximum number of concurrent workers.
        log_level: Logging level.
    """

    app_name: str = "recon-tool"
    debug: bool = False
    timeout_default: float = 1.0
    max_workers: int = 100
    log_level: str = "INFO"

    # Top 20 most common ports according to Nmap
    TOP_PORTS: list[int] = [
        21, 22, 23, 25, 53, 80, 110, 135, 139, 143,
        443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

# Basic logging configuration
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("recon")
