import pytest
from unittest.mock import patch, MagicMock

from app.game.Bishop import Bishop
from app.game.King import King
from app.game.Knight import Knight
from app.game.Pawn import Pawn
from app.game.Queen import Queen
from app.game.Rook import Rook
from app.game.pieces import Piece
from app.game import Colour


@pytest.fixture
@patch('pygame.image.load')
@patch('pygame.transform.scale')
def mock_piece_classes(mock_scale, mock_load):
    """Fixture to mock piece initialization with pygame dependencies"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()


def test_pawn_valid_moves(mock_piece_classes):
    """Test Pawn's valid moves including forward and diagonal captures"""
    # Create a mock 8x8 chess board
    board = [[None for _ in range(8)] for _ in range(8)]

    # Place a white pawn at (6, 4)
    white_pawn = Pawn(position=(6, 4), colour=Colour.WHITE, square_size=80)
    board[6][4] = white_pawn

    # Test that it can move forward by 1 or 2 squares if not blocked
    moves = white_pawn.valid_moves(board)
    assert (5, 4) in moves  # Move one square forward
    assert (4, 4) in moves  # Move two squares forward (first move)

    # Block the pawn's forward move and check no forward moves
    board[5][4] = Pawn(position=(5, 4), colour=Colour.BLACK, square_size=80)
    moves = white_pawn.valid_moves(board)
    assert (5, 4) not in moves  # Blocked by a piece

    # Test diagonal capture
    board[5][3] = Pawn(position=(5, 3), colour=Colour.BLACK, square_size=80)  # Enemy on diagonal
    moves = white_pawn.valid_moves(board)
    assert (5, 3) in moves  # Diagonal capture allowed


def test_rook_valid_moves(mock_piece_classes):
    """Test Rook's valid moves including horizontal and vertical movement"""
    board = [[None for _ in range(8)] for _ in range(8)]

    # Place a black rook at (0, 0)
    black_rook = Rook(position=(0, 0), colour=Colour.BLACK, square_size=80)
    board[0][0] = black_rook

    # Rook should be able to move along the entire row and column
    moves = black_rook.valid_moves(board)
    expected_moves = [(i, 0) for i in range(1, 8)] + [(0, j) for j in range(1, 8)]
    assert all(move in moves for move in expected_moves)

    # Block the rook's path and test that it can't move past other pieces
    board[0][3] = Rook(position=(0, 3), colour=Colour.BLACK, square_size=80)  # Friendly piece
    board[3][0] = Pawn(position=(3, 0), colour=Colour.WHITE, square_size=80)  # Enemy piece
    moves = black_rook.valid_moves(board)
    assert (0, 3) not in moves  # Blocked by friendly piece
    assert (3, 0) in moves  # Can capture enemy piece


def test_knight_valid_moves(mock_piece_classes):
    """Test Knight's valid moves including jumps in 'L' shapes"""
    board = [[None for _ in range(8)] for _ in range(8)]

    # Place a knight at (3, 3)
    knight = Knight(position=(3, 3), colour=Colour.WHITE, square_size=80)
    board[3][3] = knight

    # Knight should be able to move in 'L' shapes
    moves = knight.valid_moves(board)
    expected_moves = [(5, 4), (5, 2), (4, 5), (4, 1), (2, 5), (2, 1), (1, 4), (1, 2)]
    assert all(move in moves for move in expected_moves)

    # Block knight's movement with friendly and enemy pieces
    board[5][4] = Pawn(position=(5, 4), colour=Colour.WHITE, square_size=80)  # Friendly piece
    board[5][2] = Pawn(position=(5, 2), colour=Colour.BLACK, square_size=80)  # Enemy piece
    moves = knight.valid_moves(board)
    assert (5, 4) not in moves  # Can't move to a spot occupied by a friendly piece
    assert (5, 2) in moves  # Can capture enemy piece


def test_bishop_valid_moves(mock_piece_classes):
    """Test Bishop's valid moves including diagonal movement"""
    board = [[None for _ in range(8)] for _ in range(8)]

    # Place a white bishop at (4, 4)
    bishop = Bishop(position=(4, 4), colour=Colour.WHITE, square_size=80)
    board[4][4] = bishop

    # Bishop should be able to move diagonally
    moves = bishop.valid_moves(board)
    expected_moves = [(5, 5), (6, 6), (7, 7), (3, 3), (2, 2), (1, 1), (0, 0),
                      (5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7)]
    assert all(move in moves for move in expected_moves)

    # Block the bishop's path with friendly and enemy pieces
    board[6][6] = Pawn(position=(6, 6), colour=Colour.WHITE, square_size=80)  # Friendly piece
    board[2][2] = Pawn(position=(2, 2), colour=Colour.BLACK, square_size=80)  # Enemy piece
    moves = bishop.valid_moves(board)
    assert (6, 6) not in moves  # Blocked by friendly piece
    assert (2, 2) in moves  # Can capture enemy piece


def test_queen_valid_moves(mock_piece_classes):
    """Test Queen's valid moves including diagonal, horizontal, and vertical movement"""
    board = [[None for _ in range(8)] for _ in range(8)]

    # Place a white queen at (3, 3)
    queen = Queen(position=(3, 3), colour=Colour.WHITE, square_size=80)
    board[3][3] = queen

    # Queen can move like both a Rook and a Bishop
    moves = queen.valid_moves(board)
    expected_moves = [(i, 3) for i in range(8) if i != 3] + [(3, j) for j in range(8) if j != 3] + \
                     [(4, 4), (5, 5), (6, 6), (7, 7), (2, 2), (1, 1), (0, 0), (4, 2), (5, 1), (6, 0), (2, 4), (1, 5)]
    assert all(move in moves for move in expected_moves)


def test_king_valid_moves(mock_piece_classes):
    """Test King's valid moves including one-step moves in all directions"""
    board = [[None for _ in range(8)] for _ in range(8)]

    # Place a white king at (4, 4)
    king = King(position=(4, 4), colour=Colour.WHITE, square_size=80)
    board[4][4] = king

    # King should be able to move one step in any direction
    moves = king.valid_moves(board)
    expected_moves = [(5, 5), (5, 4), (5, 3), (4, 5), (4, 3), (3, 5), (3, 4), (3, 3)]
    assert all(move in moves for move in expected_moves)

    # Block the king's movement with friendly pieces and check it's valid
    board[5][5] = Pawn(position=(5, 5), colour=Colour.WHITE, square_size=80)  # Friendly piece
    moves = king.valid_moves(board)
    assert (5, 5) not in moves  # Can't move to a spot occupied by a friendly piece