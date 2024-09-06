import pygame
import os

from app import get_board_asset_path
from .King import King
from .Queen import Queen
from .Bishop import Bishop
from .Knight import Knight
from .Rook import Rook
from .Pawn import Pawn

from . import Colour, is_in_bounds
import copy


class Board:
    def __init__(self, screen_width, screen_height):
        # Game Screen width and Height
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load board png and scale it to screen dimensions
        try:
            self.sprite = pygame.transform.scale(pygame.image.load(get_board_asset_path()),
                                                 (screen_width, screen_height))
        except pygame.error as e:
            print(f"Error loading board image: {e}")
            self.sprite = None

        # Initialise game board
        self._empty_board = [[None for _ in range(8)] for _ in range(8)]
        self.board = copy.deepcopy(self._empty_board)
        self.old_board = copy.deepcopy(self._empty_board)
        self.pieces = []
        self.turn = Colour.WHITE
        self.selected_piece = None
        self.check = False

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

    def _place_pieces(self, piece_class, positions, colour):
        """Helper to place a row of pieces on the board"""
        for pos in positions:
            self._add_piece(piece_class, pos, colour)

    def _add_piece(self, piece_class, position, colour):
        """Adds a piece to the board and the piece list"""
        piece = piece_class(position=position, colour=colour, square_size=self.square_size_x)
        self.pieces.append(piece)
        self.board[position[0]][position[1]] = piece

    def setup_board(self):
        """
        Initialises the board. Adds starting position of each piece.
        """

        self._place_pieces(Pawn, [(1, i) for i in range(8)], Colour.BLACK)
        self._place_pieces(Pawn, [(6, i) for i in range(8)], Colour.WHITE)

        piece_positions = {
            Rook: [(0, 0), (0, 7), (7, 0), (7, 7)],
            Knight: [(0, 1), (0, 6), (7, 1), (7, 6)],
            Bishop: [(0, 2), (0, 5), (7, 2), (7, 5)],
            Queen: [(0, 3), (7, 3)],
            King: [(0, 4), (7, 4)]
        }

        for piece_class, positions in piece_positions.items():
            for pos in positions:
                colour = Colour.BLACK if pos[0] == 0 else Colour.WHITE
                self._add_piece(piece_class, pos, colour)

    def move_piece(self, piece, new_position):
        print(f"MOVING: {piece.__class__.__name__}")
        if not is_in_bounds(*new_position):
            print("Invalid move: Out of bounds")
            return
        if not self.is_valid_move(piece, new_position):
            print("Invalid move: Move not allowed for piece")
            return

        # Simulate move to see if it results in check
        old_position = piece.position
        piece.position = new_position
        new_position_current_piece = self.board[new_position[0]][new_position[1]]
        self.board[piece.position[0]][piece.position[1]] = None
        self.board[new_position[0]][new_position[1]] = piece
        threats = self.is_check(self.turn)
        self.board[piece.position[0]][piece.position[1]] = piece
        self.board[new_position[0]][new_position[1]] = new_position_current_piece
        piece.position = old_position

        if threats:
            print("Invalid move: Leaves game in check")
            return



        old_position = piece.position
        piece.position = new_position
        piece.has_moved = True
        self.board[old_position[0]][old_position[1]] = None
        self.board[new_position[0]][new_position[1]] = piece
        self.turn = Colour.WHITE if self.turn == Colour.BLACK else Colour.BLACK

        # TODO: Better management of self.pieces. Calling it every move piece is inefficient
        self.pieces = [playing_piece for row in self.board for playing_piece in row if playing_piece is not None]

    def find_king(self, colour):
        """Find the position of the king of a given colour"""
        for row in self.board:
            for piece in row:
                if isinstance(piece, King):
                    if piece.colour == colour:
                        return piece.position
        return None

    @staticmethod
    def get_positions_between(start, end):
        """Returns all the positions between two points"""
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

    def can_capture(self, attacker):
        """Check if any piece can capture the attacker"""
        for row in self.board:
            for piece in row:
                if piece is not None and piece.colour != attacker.colour:
                    if attacker.position in piece.valid_moves(self.board):
                        return True
        return False

    def can_block(self, attacker, king):
        """Check if any piece can block the attacker"""
        if isinstance(attacker, (Rook, Bishop, Queen)):

            # Get all positions we can move to block
            positions_to_block = self.get_positions_between(attacker.position, king.position)

            for row in self.board:
                for piece in row:
                    if piece is not None and piece.colour == king.colour:
                        for move in piece.valid_moves(self.board):
                            if move in positions_to_block:
                                return True

        return False

    def is_check(self, colour: Colour) -> list:
        """Checks to see if given colour is in check"""
        threats = []
        king_position = self.find_king(colour)
        if king_position is None:
            return threats  # This should never happen

        # Loop through enemy pieces and see if any can attack the king
        for row in self.board:
            for piece in row:
                if piece is not None and piece.colour != colour:
                    if piece.can_attack(self.board, king_position):
                        threats.append(piece)
        return threats

    def is_checkmate(self) -> bool:
        """Checks for check mate. Will be called at end of every move to see if Game over"""

        # Check if King is in check (checks if there exist any attacking pieces)
        attacking_pieces = self.is_check(self.turn)
        if not attacking_pieces:
            return False

        king_position = self.find_king(self.turn)
        king_piece = self.board[king_position[0]][king_position[1]]

        # Checks if King has any valid moves to escape check
        if king_piece.valid_moves(self.board):
            return False

        # Check to see if the attackers can be captured or blocked
        for attacker in attacking_pieces:
            if self.can_capture(attacker) or self.can_block(attacker, king_piece):
                return False

        return True


    @staticmethod
    def is_stalemate(self) -> bool:
        return False

    def is_game_over(self) -> bool:
        return self.is_stalemate('') or self.is_checkmate()

    def render(self, screen):
        """Renders the board and all active pieces"""
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

        if is_in_bounds(board_x, board_y):
            return self.board[int(board_x)][int(board_y)]

    def is_valid_move(self, piece, position):
        valid_moves = piece.valid_moves(self.board)
        return position in valid_moves

    def is_check_mate(self) -> bool:
        return False

    def handle_click(self, position):
        pass
