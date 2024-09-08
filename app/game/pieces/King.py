from app.game import is_in_bounds
from .pieces import Piece
from app import get_piece_asset_path


class King(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, "King")
        super().__init__(position, colour, sprite_path, square_size)

    def position_is_check(self, board: dict, new_position) -> bool:
        """
        Simulates moving the King to a new position and checks if the position is under attack.

        :param board: The current state of the chess board.
        :param new_position: The position to check for attack.
        :return: True if the new position is in check, False otherwise.
        """
        original_piece = board.get(new_position, None)

        # Simulate move
        board.pop(self.position)
        board[new_position] = self

        # Check if any opposing piece can attack the new position
        in_check = any(
            piece.colour != self.colour and piece.can_attack(board, new_position)
            for piece in board.values()
        )

        # Revert the simulated move
        board[self.position] = self
        if original_piece is not None:
            board[new_position] = original_piece
        else:
            board.pop(new_position)

        return in_check

    def can_attack(self, board, target_position) -> bool:
        """
        Checks if the King can attack a specific position on the board.

        :param board: The current state of the chess board.
        :param target_position: The position to check for attack.
        :return: True if the King can attack the target position, False otherwise.
        """
        return target_position in self._generate_king_moves()

    def _valid_moves(self, board) -> list:
        """
        Returns all valid moves for the King, taking into account checks.

        :param board: The current state of the chess board.
        :return: A list of valid positions (as (ROW, COL)) where the King can move.
        """
        moves = [
            (new_row, new_col)
            for new_row, new_col in self._generate_king_moves()
            if (new_row, new_col) not in board.keys() or board[(new_row, new_col)].colour != self.colour
        ]

        # Filter out moves that would put the King in check
        return [move for move in moves if not self.position_is_check(board, move)]

    def _generate_king_moves(self) -> list:
        """
        Generates potential moves for the King, without considering checks.

        :param board: The current state of the chess board.
        :return: A list of potential positions (as (ROW, COL)) where the King could move.
        """
        ROW, COL = self.position
        steps = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]

        return [
            (ROW + drow, COL + dcol)
            for drow, dcol in steps
            if is_in_bounds(ROW + drow, COL + dcol)
        ]

    # TODO: Add castling functionality
