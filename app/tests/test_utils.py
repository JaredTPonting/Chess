import os
import pytest
from unittest.mock import patch
from app.game import Colour
from app import get_board_asset_path, get_piece_asset_path


@patch('os.path.abspath')
@patch('os.path.dirname')
def test_get_board_asset_path(mock_dirname, mock_abspath):
    """Test the path returned by get_board_asset_path"""

    # Mock the base path to simulate different environments
    mock_abspath.return_value = "\\mock\\base\\path"
    mock_dirname.return_value = "\\mock\\base\\path"

    expected_path = "\\mock\\base\\path\\gui\\assets\\boards\\board_plain_01.png"
    result = get_board_asset_path()

    assert result == expected_path, f"Expected: {expected_path}, but got: {result}"


@patch('os.path.abspath')
@patch('os.path.dirname')
def test_get_piece_asset_path(mock_dirname, mock_abspath):
    """Test the path returned by get_piece_asset_path for different pieces and colors"""

    # Mock the base path to simulate different environments
    mock_abspath.return_value = "\\mock\\base\\path"
    mock_dirname.return_value = "\\mock\\base\\path"

    # Test for a white pawn
    expected_path = "\\mock\\base\\path\\gui\\assets\\16x32 pieces\\W_Pawn.png"
    result = get_piece_asset_path(Colour.WHITE, 'Pawn')
    assert result == expected_path, f"Expected: {expected_path}, but got: {result}"

    # Test for a black rook
    expected_path = "\\mock\\base\\path\\gui\\assets\\16x32 pieces\\B_Rook.png"
    result = get_piece_asset_path(Colour.BLACK, 'Rook')
    assert result == expected_path, f"Expected: {expected_path}, but got: {result}"

    # Test for a white knight
    expected_path = "\\mock\\base\\path\\gui\\assets\\16x32 pieces\\W_Knight.png"
    result = get_piece_asset_path(Colour.WHITE, 'Knight')
    assert result == expected_path, f"Expected: {expected_path}, but got: {result}"

    # Test for a black queen
    expected_path = "\\mock\\base\\path\\gui\\assets\\16x32 pieces\\B_Queen.png"
    result = get_piece_asset_path(Colour.BLACK, 'Queen')
    assert result == expected_path, f"Expected: {expected_path}, but got: {result}"
