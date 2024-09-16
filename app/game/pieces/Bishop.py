from typing import List, Union
from app import get_piece_asset_path
from app.game import is_in_bounds
from app.game.pieces.pieces import Piece
from app.game import Colour


class Bishop(Piece):
    def __init__(self, position: tuple[int, int], colour: Colour, square_size: int):
        """
        Initializes the Bishop piece with its position, colour, and sprite.

        :param position: Tuple of (ROW, COL) representing the initial position of the bishop on the board.
        :param colour: The colour of the bishop (either black or white).
        :param square_size: The size of the square on the chessboard.
        """
        sprite_path = get_piece_asset_path(colour, "Bishop")
        super().__init__(position, colour, sprite_path, square_size)

    def _valid_moves(self, board, enpassant) -> List[tuple[int, int]]:
        """
        Returns a list of valid moves for the bishop.
        Bishops move diagonally in all four directions and can continue moving in a direction
        until they hit another piece or the edge of the board.

        :param board: 2D list representing the chessboard, with either a Piece or None in each square.
        :return: A list of valid move positions as (ROW, COL) tuples.
        """
        moves = []
        ROW, COL = self.position

        # Bishop moves diagonally in four directions
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for drow, dcol in directions:
            new_row, new_col = ROW, COL

            while True:
                new_row += drow
                new_col += dcol

                if not is_in_bounds(new_row, new_col):
                    break  # Stop if out of bounds

                # If the square is empty, add it to valid moves
                if (new_row, new_col) not in board.keys():
                    moves.append((new_row, new_col))

                # If the square has an opponent's piece, add it to valid moves and stop further movement
                elif board[(new_row, new_col)].colour != self.colour:
                    moves.append((new_row, new_col))
                    break  # Bishop cannot jump over pieces

                # If the square has a piece of the same colour, stop
                else:
                    break

        return moves
