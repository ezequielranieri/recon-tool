"""Unit tests for network utilities."""

import socket
from unittest.mock import MagicMock, patch

import pytest

from recon.utils.network import conectar_seguro, es_puerto_abierto


class TestNetworkUtils:
    """Test suite for network utilities."""

    def test_es_puerto_abierto_true(self):
        """Verifies detection of an open port."""
        with patch("socket.socket") as mock_socket:
            mock_socket.return_value.__enter__.return_value.connect_ex.return_value = 0
            assert es_puerto_abierto("127.0.0.1", 80) is True

    def test_es_puerto_abierto_false(self):
        """Verifies detection of a closed port."""
        with patch("socket.socket") as mock_socket:
            mock_socket.return_value.__enter__.return_value.connect_ex.return_value = 111
            assert es_puerto_abierto("127.0.0.1", 80) is False

    def test_conectar_seguro_exito(self):
        """Verifies successful connection."""
        with patch("socket.socket") as mock_socket:
            mock_obj = MagicMock()
            mock_socket.return_value = mock_obj
            
            sock = conectar_seguro("127.0.0.1", 80)
            assert sock == mock_obj
            mock_obj.connect.assert_called_once_with(("127.0.0.1", 80))

    def test_conectar_seguro_timeout(self):
        """Verifies timeout handling in connection."""
        with patch("socket.socket") as mock_socket:
            mock_obj = MagicMock()
            mock_obj.connect.side_effect = socket.timeout
            mock_socket.return_value = mock_obj
            
            with pytest.raises(ConnectionError, match="Timeout"):
                conectar_seguro("127.0.0.1", 80)
            mock_obj.close.assert_called_once()
