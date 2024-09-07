from app import get_piece_asset_path
from app.game import is_in_bounds
from app.game.pieces import Piece


class Queen(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, "Queen")
        super().__init__(position, colour, sprite_path, square_size)

    def valid_moves(self, board) -> list:
        """
        Returns all valid moves for the Queen.

        The Queen can move diagonally, horizontally, and vertically. This method computes all valid moves
        based on these movement patterns.

        :param board: The current state of the chess board.
        :return: A list of valid positions (as (ROW, COL)) where the Queen can move.
        """
        moves = []
        ROW, COL = self.position

        # Queen's movement directions (diagonal, horizontal, and vertical)
        directions = [
            (1, 1),   # Diagonal down-right
            (1, -1),  # Diagonal down-left
            (-1, 1),  # Diagonal up-right
            (-1, -1), # Diagonal up-left
            (1, 0),   # Down
            (-1, 0),  # Up
            (0, 1),   # Right
            (0, -1)   # Left
        ]

        # Iterate over all possible directions
        for drow, dcol in directions:
            new_row, new_col = ROW, COL

            # Continue moving in the current direction until an obstacle is encountered
            while True:
                new_row += drow
                new_col += dcol

                if not is_in_bounds(new_row, new_col):
                    # Stop if move is out of bounds
                    break

                target_piece = board[new_row][new_col]

                if target_piece is None:
                    # Add the position if it's an empty square
                    moves.append((new_row, new_col))
                elif target_piece.colour != self.colour:
                    # Capture opponent's piece and stop moving in this direction
                    moves.append((new_row, new_col))
                    break
                else:
                    # Blocked by own piece, stop moving in this direction
                    break

        return moves
