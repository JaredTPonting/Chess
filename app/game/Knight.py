from app import get_piece_asset_path
from app.game import is_in_bounds
from app.game.pieces import Piece


class Knight(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, "Knight")
        super().__init__(position, colour, sprite_path, square_size)

    def _valid_moves(self, board) -> list:
        """
        Returns all valid moves for the Knight.

        :param board: The current state of the chess board.
        :return: A list of valid positions (as (ROW, COL)) where the Knight can move.
        """
        moves = []
        ROW, COL = self.position
        # Possible moves for the knight (L-shaped jumps)
        jumps = [(2, -1), (2, 1), (-2, -1), (-2, 1), (1, 2), (-1, 2), (1, -2), (-1, -2)]

        for drow, dcol in jumps:
            new_row, new_col = ROW + drow, COL + dcol

            if not is_in_bounds(new_row, new_col):
                # Skip if the move is out of bounds
                continue

            target_piece = board[new_row][new_col]

            if target_piece is None:
                # Move to empty square
                moves.append((new_row, new_col))
            elif target_piece.colour != self.colour:
                # Capture opponent's piece
                moves.append((new_row, new_col))

        return moves
