from typing import Union, List

from app import get_piece_asset_path

import pygame
import os


class Piece:
    def __init__(self, position, colour, sprite_path):
        self.position = position
        self.colour = colour
        self.sprite = pygame.image.load(sprite_path)
        self.has_moved = False

    def move(self, new_position):
        self.position = new_position
        self.has_moved = True

    def valid_moves(self, board):
        raise NotImplementedError("This method should be overwritten in subclasses")

    @staticmethod
    def is_in_bounds(x: int, y: int) -> bool:
        """
        Checks whether the x, y position of move is within bounds of the board

        :param x: Potential X position of Piece
        :param y: Potential Y position of Piece
        :return:  (bool) True if position is in bounds
        """
        return 0 <= x <= 8 and 0 <= y <= 8


class Pawn(Piece):
    def __init__(self, position, colour):
        sprite_path = get_piece_asset_path(colour, 'Pawn')
        super().__init__(position, colour, sprite_path)
        self.direction = 1 if self.colour == "BLACK" else -1

    def valid_moves(self, board: List[List[Union[Piece, None]]]):
        moves = []
        x, y = self.position

        # Move PAWN one square forward
        next_x = x + self.direction
        if self.is_in_bounds(next_x, y) and board[next_x][y] is None:
            moves.append((next_x, y))

        # First move only. Move PAWN two squares forward
        if not self.has_moved:
            next_2_x = next_x + self.direction
            if self.is_in_bounds(next_2_x, y) and board[next_2_x][y] is None:
                moves.append((next_2_x, y))

        # Capture Moves
        for dy in [-1, 1]:
            next_y = y + dy
            if self.is_in_bounds(next_x, next_y) and board[next_x][next_y] is not None:
                if board[next_x][next_y].colour != self.colour:
                    moves.append((next_x, next_y))

        # Add en passant.

        # PROMOTION WILL BE HANDLED WITHIN BOARD
