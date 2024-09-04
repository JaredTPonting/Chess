import pygame
import os

from pieces import Pawn, Rook, Knight, Bishop, King, Queen


class Board:
    def __int__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.pieces = []
        self.turn = "WHITE"
        self.selected_piece = None
        self.setup_board()

    def setup_board(self):

        # Set up Pawns
        for i in range(8):
            self.board[1][i] = Pawn(position=(1, i), colour="BLACK")
            self.board[6][i] = Pawn(position=(6, i), colour="WHITE")

        # Set up Rooks
        self.board[0][0] = Rook((0, 0), 'BLACK')
        self.board[0][7] = Rook((0, 7), 'BLACK')
        self.board[7][0] = Rook((7, 0), 'WHITE')
        self.board[7][7] = Rook((7, 7), 'WHITE')

        # Set up Knights
        self.board[0][1] = Knight((0, 1), 'BLACK')
        self.board[0][6] = Knight((0, 6), 'BLACK')
        self.board[7][1] = Knight((7, 1), 'WHITE')
        self.board[7][6] = Knight((7, 6), 'WHITE')

        # Set up Bishops
        self.board[0][2] = Bishop((0, 2), 'BLACK')
        self.board[0][5] = Bishop((0, 5), 'BLACK')
        self.board[7][2] = Bishop((7, 2), 'WHITE')
        self.board[7][5] = Bishop((7, 5), 'WHITE')

        # Set up Queens
        self.board[0][3] = Queen((0, 3), 'black')
        self.board[7][3] = Queen((7, 3), 'white')

        # Set up Kings
        self.board[0][4] = King((0, 4), 'black')
        self.board[7][4] = King((7, 4), 'white')

        pass

    def move_piece(self, piece, new_position):
        pass

    def render(self, screen):
        for piece in self.pieces:
            screen.blit(piece.sprite, piece.position)

    def handle_click(self, position):
        pass
