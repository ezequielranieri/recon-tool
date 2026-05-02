"""Unit tests for the banner grabbing module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from recon.core.banner import capturar_banner, sanitizar_banner


def test_sanitizar_banner_basico():
    """Tests banner sanitization with special characters."""
    banner_sucio = "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1\r\n"
    assert sanitizar_banner(banner_sucio) == "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1"


def test_sanitizar_banner_caracteres_no_imprimibles():
    """Tests removal of non-printable characters."""
    banner_con_basura = "Welcome\x00\x01\x02to Server"
    assert sanitizar_banner(banner_con_basura) == "Welcometo Server"


@pytest.mark.asyncio
async def test_capturar_banner_exito():
    """Verifies successful banner capture."""
    mock_reader = AsyncMock()
    mock_reader.read.return_value = b"SSH-2.0-OpenSSH_8.9"
    mock_writer = MagicMock()
    mock_writer.wait_closed = AsyncMock()

    with patch(
        "asyncio.open_connection", AsyncMock(return_value=(mock_reader, mock_writer))
    ):
        banner = await capturar_banner("127.0.0.1", 22, timeout=0.1)
        assert banner == "SSH-2.0-OpenSSH_8.9"


@pytest.mark.asyncio
async def test_capturar_banner_timeout():
    """Verifies that it returns None on a read timeout."""
    mock_reader = AsyncMock()
    # Simulate timeout on read
    mock_reader.read.side_effect = TimeoutError()
    mock_writer = MagicMock()
    mock_writer.wait_closed = AsyncMock()

    with patch(
        "asyncio.open_connection", AsyncMock(return_value=(mock_reader, mock_writer))
    ):
        banner = await capturar_banner("127.0.0.1", 22, timeout=0.1)
        assert banner is None
