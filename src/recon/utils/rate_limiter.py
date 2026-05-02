"""Módulo para el control de velocidad (rate limiting) de las peticiones."""

import asyncio
from collections import deque
from time import monotonic


class RateLimiter:
    """Limita la cantidad de peticiones por ventana de tiempo.

    Esta clase asegura que no se superen los límites impuestos para evitar
    bloqueos o abusos en sistemas externos.
    """

    def __init__(self, max_requests: int, ventana_segundos: float):
        """Inicializa el limitador.

        Args:
            max_requests: Número máximo de peticiones permitidas.
            ventana_segundos: Ventana de tiempo en segundos.
        """
        self.max_requests = max_requests
        self.ventana = ventana_segundos
        self.timestamps: deque[float] = deque()

    async def adquirir(self) -> None:
        """Adquiere un espacio en el limitador, esperando si es necesario.

        Calcula el tiempo de espera basado en las peticiones anteriores
        dentro de la ventana de tiempo actual.
        """
        ahora = monotonic()

        # Limpiar timestamps que están fuera de la ventana
        while self.timestamps and ahora - self.timestamps[0] > self.ventana:
            self.timestamps.popleft()

        # Si alcanzamos el límite, esperar hasta que el más antiguo salga de la ventana
        if len(self.timestamps) >= self.max_requests:
            espera = self.ventana - (ahora - self.timestamps[0])
            if espera > 0:
                await asyncio.sleep(espera)
            # Volver a verificar recursivamente después de dormir
            await self.adquirir()
            return

        self.timestamps.append(monotonic())
