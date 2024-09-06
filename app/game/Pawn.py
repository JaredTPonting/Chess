from typing import List, Union

from app import get_piece_asset_path
from app.game.pieces import Piece
from . import Colour, is_in_bounds


class Pawn(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, 'Pawn')
        super().__init__(position, colour, sprite_path, square_size)
        self.direction = 1 if self.colour == Colour.BLACK else -1

    def valid_moves(self, board: List[List[Union[Piece, None]]]) -> List[tuple]:
        moves = []
        ROW, COL = self.position

        # Move PAWN one square forward
        next_ROW = ROW + self.direction
        if is_in_bounds(next_ROW, COL) and board[next_ROW][COL] is None:
            moves.append((next_ROW, COL))

        # First move only. Move PAWN two squares forward
        if not self.has_moved:
            next_2_ROW = next_ROW + self.direction
            if is_in_bounds(next_2_ROW, COL) and board[next_2_ROW][COL] is None:
                moves.append((next_2_ROW, COL))

        # Capture Moves
        for dcol in [-1, 1]:
            next_COL = COL + dcol
            if is_in_bounds(next_ROW, next_COL) and board[next_ROW][next_COL] is not None:
                if board[next_ROW][next_COL].colour != self.colour:
                    moves.append((next_ROW, next_COL))

        # TODO: add enpassant to this method

        return moves

    def can_attack(self, board, target_position):
        # TODO: add enpassant to this method

        ROW, COL = self.position
        trow, tcol = target_position
        return trow == ROW + self.direction and (tcol == COL + 1 or tcol == COL - 1)