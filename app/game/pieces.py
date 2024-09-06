from typing import Union, List

from app import get_piece_asset_path
from abc import ABC, abstractmethod

import pygame

from . import Colour, is_in_bounds


class Piece(ABC):
    def __init__(self, position: tuple[int, int], colour: Colour, sprite_path: str, square_size: int):
        self.actual_y = None
        self.actual_x = None
        self.position = position
        self.colour = colour
        self.has_moved = False
        self.square_size = square_size

        # Load sprite with error handling
        try:
            self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (0.5 * square_size, square_size))
        except pygame.error as e:
            print(f"Error loading sprite: {e}")
            self.sprite = None

    def render(self, screen, position):
        piece_x, piece_y = position
        self.actual_x = position[0]
        self.actual_y = position[1]
        screen.blit(self.sprite, (piece_y, piece_x))

    def move(self, new_position: tuple[int, int]):
        self.position = new_position
        self.has_moved = True

    @abstractmethod
    def valid_moves(self, board):
        """
        Checks board for all valid moves for current piece
        :param board:
        :return: (List[(ROW, COL)]) List of all valid moves (ROW: int, COL: int)
        """
        raise NotImplementedError("This method should be overwritten in subclasses")

    def can_attack(self, board, target_position):
        """
        Checks whether piece can attack target position
        :param board:
        :param target_position: (x: int, y: int)
        :return:
        """
        return target_position in self.valid_moves(board)

    @staticmethod
    def is_in_bounds(x: int, y: int) -> bool:
        """
        Checks whether the x, y position of move is within bounds of the board

        :param x: Potential X position of Piece
        :param y: Potential Y position of Piece
        :return:  (bool) True if position is in bounds
        """
        return 0 <= x < 8 and 0 <= y < 8




















if __name__ == "__main__":
    print("...DONE...")
