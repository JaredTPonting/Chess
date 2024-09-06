from enum import Enum


class Colour(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"


def is_in_bounds(x: int, y: int) -> bool:
    """
    Checks whether the x, y position of move is within bounds of the board

    :param x: Potential X position of Piece
    :param y: Potential Y position of Piece
    :return:  (bool) True if position is in bounds
    """
    return 0 <= x < 8 and 0 <= y < 8
