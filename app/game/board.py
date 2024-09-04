import pygame
import os

from app import get_board_asset_path
from .pieces import Pawn, Rook, Knight, Bishop, King, Queen


class Board:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.square_size = screen_width // 8
        self.sprite = pygame.transform.scale(pygame.image.load(get_board_asset_path()), (screen_width, screen_height))
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.pieces = []
        self.turn = "WHITE"
        self.selected_piece = None
        self.setup_board()

    def setup_board(self):

        # Set up Pawns
        for i in range(8):
            self.board[1][i] = Pawn(position=(1, i), colour="BLACK", square_size=self.square_size)
            self.board[6][i] = Pawn(position=(6, i), colour="WHITE", square_size=self.square_size)

        # Set up Rooks
        self.board[0][0] = Rook((0, 0), 'BLACK', square_size=self.square_size)
        self.board[0][7] = Rook((0, 7), 'BLACK', square_size=self.square_size)
        self.board[7][0] = Rook((7, 0), 'WHITE', square_size=self.square_size)
        self.board[7][7] = Rook((7, 7), 'WHITE', square_size=self.square_size)

        # Set up Knights
        self.board[0][1] = Knight((0, 1), 'BLACK', square_size=self.square_size)
        self.board[0][6] = Knight((0, 6), 'BLACK', square_size=self.square_size)
        self.board[7][1] = Knight((7, 1), 'WHITE', square_size=self.square_size)
        self.board[7][6] = Knight((7, 6), 'WHITE', square_size=self.square_size)

        # Set up Bishops
        self.board[0][2] = Bishop((0, 2), 'BLACK', square_size=self.square_size)
        self.board[0][5] = Bishop((0, 5), 'BLACK', square_size=self.square_size)
        self.board[7][2] = Bishop((7, 2), 'WHITE', square_size=self.square_size)
        self.board[7][5] = Bishop((7, 5), 'WHITE', square_size=self.square_size)

        # Set up Queens
        self.board[0][3] = Queen((0, 3), 'black', square_size=self.square_size)
        self.board[7][3] = Queen((7, 3), 'white', square_size=self.square_size)

        # Set up Kings
        self.board[0][4] = King((0, 4), 'black', square_size=self.square_size)
        self.board[7][4] = King((7, 4), 'white', square_size=self.square_size)

        pass

    def move_piece(self, piece, new_position):
        pass

    def render(self, screen):
        screen.blit(self.sprite, dest=(0, 0))
        for row in self.board:
            for piece in row:
                if piece is None:
                    continue
                piece_x, piece_y = piece.position
                piece_x *= self.square_size
                piece_y *= self.square_size
                screen.blit(piece.sprite, (piece_y, piece_x))

    def handle_click(self, position):
        pass
