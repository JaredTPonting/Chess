from typing import Union, List, Tuple
from app import get_piece_asset_path
from abc import ABC, abstractmethod
import pygame
from . import Colour


class Piece(ABC):
    """
    Abstract base class representing a generic chess piece.
    """

    def __init__(self, position: Tuple[int, int], colour: Colour, sprite_path: str, square_size: int):
        """
        Initializes the Piece with a position, color, sprite, and size.

        :param position: Tuple representing the (row, col) position on the board.
        :param colour: Colour enum representing the piece's color (e.g., WHITE or BLACK).
        :param sprite_path: File path to the image of the piece's sprite.
        :param square_size: The size of each square on the chessboard.
        """
        self.position = position
        self.colour = colour
        self.has_moved = False
        self.square_size = square_size
        self.actual_x = None  # The actual pixel position on the screen (x-coordinate)
        self.actual_y = None  # The actual pixel position on the screen (y-coordinate)

        # Load the piece's sprite
        try:
            self.sprite = pygame.transform.scale(
                pygame.image.load(sprite_path), (int(0.5 * square_size), square_size)
            )
        except pygame.error as e:
            print(f"Error loading sprite: {e}")
            self.sprite = None

    def render(self, screen, position: Tuple[int, int]):
        """
        Renders the piece on the board at the given pixel position.

        :param screen: The Pygame screen where the piece will be rendered.
        :param position: Tuple (x, y) representing the piece's actual pixel position.
        """
        self.actual_x, self.actual_y = position
        if self.sprite:
            screen.blit(self.sprite, (self.actual_y, self.actual_x))

    def move(self, new_position: Tuple[int, int]):
        """
        Updates the piece's position on the board.

        :param new_position: Tuple (row, col) representing the new board position of the piece.
        """
        self.position = new_position
        self.has_moved = True

    def can_attack(self, board: List[List[Union['Piece', None]]], target_position: Tuple[int, int]) -> bool:
        """
        Determines if the piece can attack the given target position on the board.

        :param board: 2D list representing the current state of the chessboard.
        :param target_position: Tuple (row, col) representing the target position.
        :return: True if the piece can attack the target position, False otherwise.
        """
        return target_position in self.valid_moves(board)

    @abstractmethod
    def valid_moves(self, board: List[List[Union['Piece', None]]]) -> List[Tuple[int, int]]:
        """
        Abstract method to be implemented by each specific piece (King, Queen, etc.)
        to return valid moves.

        :param board: 2D list representing the current state of the chessboard.
        :return: List of valid moves for the piece, represented as (row, col) tuples.
        """
        raise NotImplementedError("This method should be implemented in subclasses")

    @staticmethod
    def is_in_bounds(x: int, y: int) -> bool:
        """
        Checks if the given (x, y) position is within the bounds of the chessboard.

        :param x: X-coordinate (column) to check.
        :param y: Y-coordinate (row) to check.
        :return: True if the position is within bounds (0-7 for both x and y), False otherwise.
        """
        return 0 <= x < 8 and 0 <= y < 8


if __name__ == "__main__":
    print("Piece class definition complete.")
