from app import get_piece_asset_path
from app.game import is_in_bounds
from app.game.pieces import Piece


class Knight(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, "Knight")
        super().__init__(position, colour, sprite_path, square_size)

    def valid_moves(self, board):
        moves = []
        ROW, COL = self.position
        jumps = [(2, -1), (2, 1), (-2, -1), (-2, 1), (1, 2), (-1, 2), (1, -2), (-1, -2)]

        for drow, dcol in jumps:
            new_row = ROW + drow
            new_col = COL + dcol

            if not is_in_bounds(new_row, new_col):
                continue
            elif board[new_row][new_col] is None:
                moves.append((new_row, new_col))
            elif board[new_row][new_col].colour != self.colour:
                moves.append((new_row, new_col))

        return moves