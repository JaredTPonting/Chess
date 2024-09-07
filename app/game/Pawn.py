from typing import List, Union
from app import get_piece_asset_path
from app.game.pieces import Piece
from . import Colour, is_in_bounds


class Pawn(Piece):
    def __init__(self, position: tuple[int, int], colour: Colour, square_size: int):
        """
        Initializes the Pawn piece with position, colour, and sprite.
        The direction is set based on the colour of the pawn:
        - White pawns move upwards (-1 direction)
        - Black pawns move downwards (+1 direction)
        """
        sprite_path = get_piece_asset_path(colour, 'Pawn')
        super().__init__(position, colour, sprite_path, square_size)
        self.direction = 1 if self.colour == Colour.BLACK else -1  # Set movement direction based on pawn colour

    def _valid_moves(self, board: List[List[Union[Piece, None]]]) -> List[tuple[int, int]]:
        """
        Returns a list of valid moves for the pawn.
        Pawns move forward (1 or 2 squares if not moved) and can capture diagonally.

        :param board: 2D list representing the board, with None or Pieces in each square.
        :return: A list of valid move positions as (ROW, COL) tuples.
        """
        moves = []
        ROW, COL = self.position

        # Move one square forward if empty
        next_ROW = ROW + self.direction
        if is_in_bounds(next_ROW, COL) and board[next_ROW][COL] is None:
            moves.append((next_ROW, COL))

        # First move: Move two squares forward if empty
        if not self.has_moved:
            next_2_ROW = next_ROW + self.direction
            if is_in_bounds(next_2_ROW, COL) and board[next_2_ROW][COL] is None:
                moves.append((next_2_ROW, COL))

        # Capture moves: Check diagonals for opponent's pieces
        for dcol in [-1, 1]:  # Check left and right diagonal
            next_COL = COL + dcol
            if is_in_bounds(next_ROW, next_COL) and board[next_ROW][next_COL] is not None:
                if board[next_ROW][next_COL].colour != self.colour:
                    moves.append((next_ROW, next_COL))

        # TODO: Add en passant functionality

        return moves

    def can_attack(self, board: List[List[Union[Piece, None]]], target_position: tuple[int, int]) -> bool:
        """
        Checks if the pawn can attack a target position (used for capturing diagonally).
        Pawns can attack one row forward and one column to the left or right.

        :param board: 2D list representing the board.
        :param target_position: (ROW, COL) target position to check.
        :return: True if pawn can attack the target position, False otherwise.
        """
        # TODO: Add en passant functionality

        ROW, COL = self.position
        trow, tcol = target_position

        return trow == ROW + self.direction and abs(tcol - COL) == 1
