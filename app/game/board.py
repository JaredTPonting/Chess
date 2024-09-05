import pygame
import os

from app import get_board_asset_path
from .pieces import Pawn, Rook, Knight, Bishop, King, Queen


class Board:
    def __init__(self, screen_width, screen_height):
        # Game Screen width and Height
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load board png and scale it to screen dimensions
        self.sprite = pygame.transform.scale(pygame.image.load(get_board_asset_path()), (screen_width, screen_height))

        # Initialise game board
        self._empty_board = [[None for _ in range(8)] for _ in range(8)]
        self.board = self._empty_board
        self.pieces = []
        self.turn = "WHITE"
        self.selected_piece = None

        # Configuration for excluding border of chess board
        self.border_ratio = 0.05

        # Calculate the active chessboard dimensions (ignoring border)
        self.board_size_x = self.screen_width * (1 - (2 * self.border_ratio))
        self.board_size_y = self.screen_height * (1 - (2 * self.border_ratio))

        # Calculate the starting position (top left) of the board
        self.board_start_x = self.screen_width * self.border_ratio
        self.board_start_y = self.screen_height * self.border_ratio

        # Each squares size is based on the scaled inner board size
        self.square_size_x = self.board_size_x // 8
        self.square_size_y = self.board_size_y // 8

        self.setup_board()

    def setup_board(self):
        """
        Initialises the board. Adds starting position of each piece.
        :return:
        """

        # Set up Pawns
        for i in range(8):
            self.pieces.append(Pawn(position=(1, i), colour="BLACK", square_size=self.square_size_x))
            self.pieces.append(Pawn(position=(6, i), colour="WHITE", square_size=self.square_size_x))

        # Set up Rooks
        self.pieces.append(Rook((0, 0), 'BLACK', square_size=self.square_size_x))
        self.pieces.append(Rook((0, 7), 'BLACK', square_size=self.square_size_x))
        self.pieces.append(Rook((7, 0), 'WHITE', square_size=self.square_size_x))
        self.pieces.append(Rook((7, 7), 'WHITE', square_size=self.square_size_x))

        # Set up Knights
        self.pieces.append(Knight((0, 1), 'BLACK', square_size=self.square_size_x))
        self.pieces.append(Knight((0, 6), 'BLACK', square_size=self.square_size_x))
        self.pieces.append(Knight((7, 1), 'WHITE', square_size=self.square_size_x))
        self.pieces.append(Knight((7, 6), 'WHITE', square_size=self.square_size_x))

        # Set up Bishops
        self.pieces.append(Bishop((0, 2), 'BLACK', square_size=self.square_size_x))
        self.pieces.append(Bishop((0, 5), 'BLACK', square_size=self.square_size_x))
        self.pieces.append(Bishop((7, 2), 'WHITE', square_size=self.square_size_x))
        self.pieces.append(Bishop((7, 5), 'WHITE', square_size=self.square_size_x))

        # Set up Queens
        self.pieces.append(Queen((0, 3), 'black', square_size=self.square_size_x))
        self.pieces.append(Queen((7, 3), 'white', square_size=self.square_size_x))

        # Set up Kings
        self.pieces.append(King((0, 4), 'black', square_size=self.square_size_x))
        self.pieces.append(King((7, 4), 'white', square_size=self.square_size_x))

        for piece in self.pieces:
            self.board[piece.position[0]][piece.position[1]] = piece

    @staticmethod
    def is_in_bounds(x: int, y: int):
        return 0 <= x < 8 and 0 <= y < 8

    def move_piece(self, piece, new_position):
        print(f"MOVING: {piece.__class__.__name__}")
        pass

    def render(self, screen):
        # Draw board
        screen.blit(self.sprite, dest=(0, 0))

        # Draw each piece
        for piece in self.pieces:
            if self.selected_piece and piece == self.selected_piece:
                continue
            piece_x, piece_y = piece.position

            # Adjust position to fit within board (excluding boarder)
            piece_x = self.board_start_x + (piece_x * self.square_size_x) - (self.square_size_x * 0.1)
            piece_y = self.board_start_y + (piece_y * self.square_size_y) + (self.square_size_y * 0.25)

            # Draw piece on board
            piece.render(screen, (piece_x, piece_y))

    def get_piece_at(self, mouse_x, mouse_y):
        board_x = (mouse_x - self.board_start_x) // self.square_size_x
        board_y = (mouse_y - self.board_start_y) // self.square_size_y

        if self.is_in_bounds(board_x, board_y):
            return self.board[int(board_x)][int(board_y)]

    def is_valid_move(self, piece, position):
        valid_moves = piece.valid_moves(self.board)
        return position in valid_moves

    def handle_click(self, position):
        pass
