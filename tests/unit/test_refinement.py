"""Tests for the new network and rate limiting utilities."""

import asyncio
import pytest
from time import monotonic
from recon.utils.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_rate_limiter_basico():
    """Verifies that the rate limiter respects limits."""
    # 2 requests per 0.5 seconds
    limiter = RateLimiter(max_requests=2, ventana_segundos=0.5)
    
    start = monotonic()
    await limiter.adquirir()  # 1
    await limiter.adquirir()  # 2
    
    # The third one must wait
    await limiter.adquirir()  # 3
    duration = monotonic() - start
    
    assert duration >= 0.45  # Approximately 0.5s


def test_redes_privadas_adicionales():
    """Verifies that additional private networks are blocked."""
    from recon.utils.validators import validar_host
    
    with pytest.raises(ValueError, match="is reserved"):
        validar_host("10.0.0.1")
        
    with pytest.raises(ValueError, match="is reserved"):
        validar_host("172.16.0.1")
        
    with pytest.raises(ValueError, match="is reserved"):
        validar_host("192.168.1.1")
