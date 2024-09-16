from app.game import is_in_bounds
from .pieces import Piece
from app import get_piece_asset_path
from copy import deepcopy


class King(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, "King")
        super().__init__(position, colour, sprite_path, square_size)

    def can_attack(self, board, target_position) -> bool:
        """
        Checks if the King can attack a specific position on the board.

        :param board: The current state of the chess board.
        :param target_position: The position to check for attack.
        :return: True if the King can attack the target position, False otherwise.
        """
        return target_position in self._generate_king_moves()

    def _valid_moves(self, board, enpassant) -> list:
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
        return moves

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
