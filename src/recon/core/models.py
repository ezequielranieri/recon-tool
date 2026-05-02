"""Data models for port scanning."""

from datetime import datetime

from pydantic import BaseModel, Field


class ResultadoPuerto(BaseModel):
    """Represents the scan result of a single port.

    Attributes:
        puerto: The scanned port number.
        estado: The detected state ("open", "closed", "filtered").
        servicio: The name of the identified service (if any).
        banner: The service banner captured (if any).
        tiempo_ms: Response time in milliseconds.
    """

    puerto: int = Field(..., ge=1, le=65535)
    estado: str
    servicio: str | None = None
    banner: str | None = None
    tiempo_ms: float


class ResultadoEscaneo(BaseModel):
    """Represents the complete scan result of a host.

    Attributes:
        host: The target hostname or IP.
        ip: The resolved IP address.
        timestamp: Scan date and time.
        duracion_segundos: Total scan duration.
        puertos_escaneados: Total amount of processed ports.
        puertos_abiertos: List of results for open ports.
        metadata: Optional additional information.
    """

    host: str
    ip: str
    timestamp: datetime = Field(default_factory=datetime.now)
    duracion_segundos: float
    puertos_escaneados: int
    puertos_abiertos: list[ResultadoPuerto] = []
    metadata: dict[str, str] = {}
