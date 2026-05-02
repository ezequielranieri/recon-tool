"""Pruebas para las nuevas utilidades de red y rate limiting."""

import asyncio
import pytest
from time import monotonic
from recon.utils.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_rate_limiter_basico():
    """Verifica que el rate limiter respeta los límites."""
    # 2 requests por 0.5 segundos
    limiter = RateLimiter(max_requests=2, ventana_segundos=0.5)
    
    start = monotonic()
    await limiter.adquirir()  # 1
    await limiter.adquirir()  # 2
    
    # La tercera debe esperar
    await limiter.adquirir()  # 3
    duration = monotonic() - start
    
    assert duration >= 0.45  # Aproximadamente 0.5s


def test_redes_privadas_adicionales():
    """Verifica que las nuevas redes privadas sean bloqueadas."""
    from recon.utils.validators import validar_host
    
    with pytest.raises(ValueError, match="está reservada"):
        validar_host("10.0.0.1")
        
    with pytest.raises(ValueError, match="está reservada"):
        validar_host("172.16.0.1")
        
    with pytest.raises(ValueError, match="está reservada"):
        validar_host("192.168.1.1")
