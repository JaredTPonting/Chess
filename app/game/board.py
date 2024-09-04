import pygame
import os

from pieces import Pawn


class Board:
    def __int__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.pieces = []
        self.turn = "WHITE"
        self.selected_piece = None
        self.setup_board()

    def setup_board(self):
        for i in range(8):
            self.grid[1][i] = Pawn((1, i), "BLACK", "")

        pass

    def move_piece(self, piece, new_position):
        pass

    def render(self, screen):
        for piece in self.pieces:
            screen.blit(piece.sprite, piece.position)

    def handle_click(self, position):
        pass
