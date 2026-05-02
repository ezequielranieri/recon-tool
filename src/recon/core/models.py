"""Modelos de datos para el escaneo de puertos."""

from datetime import datetime

from pydantic import BaseModel, Field


class ResultadoPuerto(BaseModel):
    """Representa el resultado del escaneo de un solo puerto.

    Attributes:
        puerto: El número del puerto escaneado.
        estado: El estado detectado ("abierto", "cerrado", "filtrado").
        servicio: El nombre del servicio identificado (si existe).
        banner: El banner capturado del servicio (si existe).
        tiempo_ms: El tiempo de respuesta en milisegundos.
    """

    puerto: int = Field(..., ge=1, le=65535)
    estado: str
    servicio: str | None = None
    banner: str | None = None
    tiempo_ms: float


class ResultadoEscaneo(BaseModel):
    """Representa el resultado completo del escaneo de un host.

    Attributes:
        host: El hostname o IP objetivo.
        ip: La dirección IP resuelta.
        timestamp: Fecha y hora del escaneo.
        duracion_segundos: Duración total del escaneo.
        puertos_escaneados: Cantidad total de puertos procesados.
        puertos_abiertos: Lista de resultados para puertos abiertos.
        metadata: Información adicional opcional.
    """

    host: str
    ip: str
    timestamp: datetime = Field(default_factory=datetime.now)
    duracion_segundos: float
    puertos_escaneados: int
    puertos_abiertos: list[ResultadoPuerto] = []
    metadata: dict[str, str] = {}
