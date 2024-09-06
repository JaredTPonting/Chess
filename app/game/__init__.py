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


def get_positions_between(start, end):
    """Return all positions between two points (for sliding pieces like Rook, Bishop, Queen)"""
    positions = []
    row_step = col_step = 0

    if start[0] < end[0]:
        row_step = 1
    elif start[0] > end[0]:
        row_step = -1

    if start[1] < end[1]:
        col_step = 1
    elif start[1] > end[1]:
        col_step = -1

    current_row, current_col = start[0] + row_step, start[1] + col_step

    while (current_row, current_col) != end:
        positions.append((current_row, current_col))
        current_row += row_step
        current_col += col_step

    return positions