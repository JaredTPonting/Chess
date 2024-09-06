# from .King import King
from . import Colour


def find_king(board, colour):
    """Find the position of the king of a given colour"""
    for row in board:
        for piece in row:
            if piece.__class__.__name__ == "King":
                if piece.colour == colour:
                    return piece.position
    return None


def is_check(board, colour: Colour) -> list:
    """Checks to see if given colour is in check"""
    threats = []
    king_position = find_king(board, colour)
    if king_position is None:
        return threats  # This should never happen

    # Loop through enemy pieces and see if any can attack the king
    for row in board:
        for piece in row:
            if piece is not None and piece.colour != colour:
                if piece.can_attack(board, king_position):
                    threats.append(piece)
    return threats
