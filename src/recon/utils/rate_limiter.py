"""Module for request rate limiting."""

import asyncio
from collections import deque
from time import monotonic


class RateLimiter:
    """Limits the number of requests per time window.

    This class ensures that imposed limits are not exceeded to avoid
    blocking or abuse in external systems.
    """

    def __init__(self, max_requests: int, ventana_segundos: float):
        """Initializes the limiter.

        Args:
            max_requests: Maximum number of allowed requests.
            ventana_segundos: Time window in seconds.
        """
        self.max_requests = max_requests
        self.ventana = ventana_segundos
        self.timestamps: deque[float] = deque()

    async def adquirir(self) -> None:
        """Acquires a slot in the limiter, waiting if necessary.

        Calculates the wait time based on previous requests
        within the current time window.
        """
        ahora = monotonic()

        # Clean timestamps that are outside the window
        while self.timestamps and ahora - self.timestamps[0] > self.ventana:
            self.timestamps.popleft()

        # If we reach the limit, wait until the oldest one leaves the window
        if len(self.timestamps) >= self.max_requests:
            espera = self.ventana - (ahora - self.timestamps[0])
            if espera > 0:
                await asyncio.sleep(espera)
            # Re-check recursively after sleeping
            await self.adquirir()
            return

        self.timestamps.append(monotonic())
