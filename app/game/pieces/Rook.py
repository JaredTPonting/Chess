from app import get_piece_asset_path
from app.game import is_in_bounds
from app.game.pieces.pieces import Piece


class Rook(Piece):
    def __init__(self, position, colour, square_size):
        """
        Initializes the Rook piece with its position, color, and sprite image.

        :param position: Initial position of the Rook on the board as a tuple (row, col).
        :param colour: The color of the Rook (black or white).
        :param square_size: The size of each square on the board for rendering the piece.
        """
        sprite_path = get_piece_asset_path(colour, 'Rook')
        super().__init__(position, colour, sprite_path, square_size)

    def _valid_moves(self, board: dict, enpassant) -> list:
        """
        Returns all valid moves for the Rook.

        The Rook moves any number of squares either horizontally or vertically. This method computes all
        valid moves based on these movement patterns.

        :param board: The current state of the chessboard.
        :return: A list of valid positions (as (ROW, COL)) where the Rook can move.
        """
        moves = []
        ROW, COL = self.position

        # Rook's movement directions (vertical and horizontal)
        directions = [
            (1, 0),  # Down
            (-1, 0), # Up
            (0, 1),  # Right
            (0, -1)  # Left
        ]

        # Iterate over each direction and calculate valid moves
        for drow, dcol in directions:
            new_row, new_col = ROW, COL

            # Keep moving in the current direction until blocked
            while True:
                new_row += drow
                new_col += dcol

                if not is_in_bounds(new_row, new_col):
                    # Stop if the move is out of bounds
                    break

                target_piece = board.get((new_row, new_col), None)

                if target_piece is None:
                    # Empty square, add move to valid moves
                    moves.append((new_row, new_col))
                elif target_piece.colour != self.colour:
                    # Capture opponent's piece and stop in this direction
                    moves.append((new_row, new_col))
                    break
                else:
                    # Blocked by own piece, stop in this direction
                    break

        return moves
