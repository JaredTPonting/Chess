import pytest
from unittest.mock import patch, MagicMock

from app.game import Colour
from app.game.pieces.Bishop import Bishop
from app.game.pieces.King import King
from app.game.pieces.Knight import Knight
from app.game.pieces.Pawn import Pawn
from app.game.pieces.Queen import Queen
from app.game.pieces.Rook import Rook
from app.game.board import Board


@pytest.fixture
def board():
    """Fixture to create a default Board object"""
    return Board(screen_width=800, screen_height=800)


@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_board_initialisation(mock_scale, mock_load, board):
    """Test broad initialisation and sprite loading"""

    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    assert board.screen_width == 800
    assert board.screen_height == 800
    assert board.sprite is not None
    assert len(board.pieces) == 32  # 16 pieces for each player
    assert board.turn == Colour.WHITE
    assert len(board.board) == 8
    assert len(board.board[0]) == 8


@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_setup_board(mock_scale, mock_load, board):
    """Test if the board is set up with the correct pieces"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    # Check that pawns are in the correct positions
    for i in range(8):
        assert isinstance(board.board[1][i], Pawn)
        assert isinstance(board.board[6][i], Pawn)

    # Check for other pieces
    assert isinstance(board.board[0][0], Rook)
    assert isinstance(board.board[0][7], Rook)
    assert isinstance(board.board[7][0], Rook)
    assert isinstance(board.board[7][7], Rook)

    assert isinstance(board.board[0][1], Knight)
    assert isinstance(board.board[0][6], Knight)
    assert isinstance(board.board[7][1], Knight)
    assert isinstance(board.board[7][6], Knight)

    assert isinstance(board.board[0][2], Bishop)
    assert isinstance(board.board[0][5], Bishop)
    assert isinstance(board.board[7][2], Bishop)
    assert isinstance(board.board[7][5], Bishop)

    assert isinstance(board.board[0][3], Queen)
    assert isinstance(board.board[7][3], Queen)

    assert isinstance(board.board[0][4], King)
    assert isinstance(board.board[7][4], King)


@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_move_piece_valid(mock_scale, mock_load, board):
    """Test valid piece move"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    # Move a pawn forward from (6, 0) to (5, 0)
    pawn = board.board[6][0]
    assert isinstance(pawn, Pawn)
    board.move_piece(pawn, (5, 0))

    # Check that the pawn was moved correctly
    assert board.board[5][0] == pawn
    assert board.board[6][0] is None
    assert pawn.position == (5, 0)
    assert pawn.has_moved is True

    # Check that the turn has changed
    assert board.turn == Colour.BLACK


@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_move_piece_out_of_bounds(mock_scale, mock_load, board):
    """Test moving a piece out of bounds"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    pawn = board.board[6][0]
    assert isinstance(pawn, Pawn)

    # Try moving the pawn to an invalid position
    board.move_piece(pawn, (8, 0))

    # The move should not happen, piece should remain at the original position
    assert board.board[6][0] == pawn


@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_get_piece_at_valid(mock_scale, mock_load, board):
    """Test retrieving a piece at a valid position"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    pawn = board.board[6][0]
    piece = board.get_piece_at(mouse_y=board.board_start_x + board.square_size_x // 2,
                               mouse_x=board.board_start_y + 6 * board.square_size_y + board.square_size_y // 2)
    assert piece == pawn


@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_get_piece_at_out_of_bounds(mock_scale, mock_load, board):
    """Test retrieving a piece at an invalid position (out of bounds)"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    piece = board.get_piece_at(mouse_x=board.board_start_x - 1, mouse_y=board.board_start_y - 1)
    assert piece is None


@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_is_valid_move(mock_scale, mock_load, board):
    """Test checking valid moves for a piece"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    pawn = board.board[6][0]
    pawn._update_moves(board.board, [])
    valid_moves = pawn.move_list

    # Let's assume pawns can move one step forward initially
    assert (5, 0) in valid_moves
    assert (4, 0) in valid_moves
    assert (5, 1) not in valid_moves


@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_get_positions_between_horizontal(mock_scale, mock_load, board):
    """Test get_positions_between for a horizontal movement"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    # Start and end points for a horizontal movement
    start = (3, 1)
    end = (3, 5)

    expected_positions = [(3, 2), (3, 3), (3, 4)]

    result = board.get_positions_between(start, end)

    assert result == expected_positions, f"Expected {expected_positions}, but got {result}"

@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_get_positions_between_vertical(mock_scale, mock_load, board):
    """Test get_positions_between for a vertical movement"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    # Start and end points for a vertical movement
    start = (1, 3)
    end = (5, 3)

    expected_positions = [(2, 3), (3, 3), (4, 3)]

    result = board.get_positions_between(start, end)

    assert result == expected_positions, f"Expected {expected_positions}, but got {result}"

@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_get_positions_between_diagonal(mock_scale, mock_load, board):
    """Test get_positions_between for a diagonal movement"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    # Start and end points for a diagonal movement
    start = (2, 2)
    end = (5, 5)

    expected_positions = [(3, 3), (4, 4)]

    result = board.get_positions_between(start, end)

    assert result == expected_positions, f"Expected {expected_positions}, but got {result}"

@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_get_positions_between_reverse_diagonal(mock_scale, mock_load, board):
    """Test get_positions_between for a reverse diagonal movement"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    # Start and end points for a reverse diagonal movement
    start = (5, 5)
    end = (2, 2)

    expected_positions = [(4, 4), (3, 3)]

    result = board.get_positions_between(start, end)

    assert result == expected_positions, f"Expected {expected_positions}, but got {result}"

@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_get_positions_between_reverse_horizontal(mock_scale, mock_load, board):
    """Test get_positions_between for a reverse horizontal movement"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    # Start and end points for a reverse horizontal movement
    start = (3, 5)
    end = (3, 1)

    expected_positions = [(3, 4), (3, 3), (3, 2)]

    result = board.get_positions_between(start, end)

    assert result == expected_positions, f"Expected {expected_positions}, but got {result}"

@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_get_positions_between_reverse_vertical(mock_scale, mock_load, board):
    """Test get_positions_between for a reverse vertical movement"""
    mock_load.return_value = MagicMock()
    mock_scale.return_value = MagicMock()

    # Start and end points for a reverse vertical movement
    start = (5, 3)
    end = (1, 3)

    expected_positions = [(4, 3), (3, 3), (2, 3)]

    result = board.get_positions_between(start, end)

    assert result == expected_positions, f"Expected {expected_positions}, but got {result}"