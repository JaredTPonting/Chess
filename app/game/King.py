from app.game import is_in_bounds
from .pieces import Piece
from app import get_piece_asset_path


class King(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, "King")
        super().__init__(position, colour, sprite_path, square_size)

    def position_is_check(self, board, new_position):
        # Simulate board move
        original_piece = board[new_position[0]][new_position[1]]
        board[self.position[0]][self.position[1]] = None
        board[new_position[0]][new_position[1]] = self
        for row in board:
            for piece in row:
                if piece is not None and piece.colour != self.colour:
                    if piece.can_attack(board, new_position):
                        # Revert board back to original
                        board[self.position[0]][self.position[1]] = self
                        board[new_position[0]][new_position[1]] = original_piece
                        return True

        board[self.position[0]][self.position[1]] = self
        board[new_position[0]][new_position[1]] = original_piece
        return False

    def can_attack(self, board, target_position):
        moves = []
        ROW, COL = self.position
        steps = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]

        for dRow, dCol in steps:
            new_row = ROW + dRow
            new_col = COL + dCol
            if not is_in_bounds(new_row, new_col):
                continue
            else:
                moves.append((new_row, new_col))

        return target_position in moves

    def valid_moves(self, board):
        moves = []
        ROW, COL = self.position

        steps = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]

        for drow, dcol in steps:
            new_row = ROW + drow
            new_col = COL + dcol

            if (not is_in_bounds(new_row, new_col)) or self.position_is_check(board, (new_row, new_col)):
                continue
            elif board[new_row][new_col] is None:
                moves.append((new_row, new_col))
            elif board[new_row][new_col].colour != self.colour:
                moves.append((new_row, new_col))

        # TODO: add castling functionality

        return moves