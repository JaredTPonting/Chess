from app import get_piece_asset_path
from app.game import is_in_bounds
from app.game.pieces import Piece


class Bishop(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, "Bishop")
        super().__init__(position, colour, sprite_path, square_size)

    def valid_moves(self, board):
        moves = []
        ROW, COL = self.position

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for drow, dcol in directions:
            new_row, new_col = ROW, COL

            while True:
                new_row += drow
                new_col += dcol

                if not is_in_bounds(new_row, new_col):
                    break

                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board[new_row][new_col].colour != self.colour:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves