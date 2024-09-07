from typing import List, Union

import pygame
import os
import copy

from app import get_board_asset_path
from .King import King
from .Queen import Queen
from .Bishop import Bishop
from .Knight import Knight
from .Rook import Rook
from .Pawn import Pawn
from . import Colour, is_in_bounds, get_positions_between


class Board:
    def __init__(self, screen_width, screen_height):
        """
        Initializes the chess board, its pieces, and relevant dimensions for rendering.
        """
        # Game screen dimensions
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load and scale the chessboard sprite
        self._load_board_image()

        # Initialize the empty board and track pieces
        self._empty_board = [[None for _ in range(8)] for _ in range(8)]
        self.board: List[List[Union[King, Queen, Bishop, Knight, Rook, Pawn, None]]] = copy.deepcopy(self._empty_board)
        self.old_board = copy.deepcopy(self._empty_board)
        self.pieces = []
        self.turn = Colour.WHITE
        self.selected_piece = None
        self.check = False

        # Configuration for chessboard border and square size
        self.border_ratio = 0.05
        self._calculate_board_dimensions()

        # Set up the initial game state
        self.setup_board()

    def _load_board_image(self):
        """Loads and scales the chessboard image."""
        try:
            self.sprite = pygame.transform.scale(
                pygame.image.load(get_board_asset_path()),
                (self.screen_width, self.screen_height)
            )
        except pygame.error as e:
            print(f"Error loading board image: {e}")
            self.sprite = None

    def _calculate_board_dimensions(self):
        """Calculates the dimensions of the active chessboard and each square."""
        # Calculate the inner board dimensions (excluding the border)
        self.board_size_x = self.screen_width * (1 - (2 * self.border_ratio))
        self.board_size_y = self.screen_height * (1 - (2 * self.border_ratio))

        # Calculate the board's starting position (top left)
        self.board_start_x = self.screen_width * self.border_ratio
        self.board_start_y = self.screen_height * self.border_ratio

        # Calculate the size of each square on the board
        self.square_size_x = self.board_size_x // 8
        self.square_size_y = self.board_size_y // 8

    def _add_piece(self, piece_class, position, colour):
        """Adds a piece to the board and the piece list."""
        piece = piece_class(position=position, colour=colour, square_size=self.square_size_x)
        self.pieces.append(piece)
        self.board[position[0]][position[1]] = piece

    def _place_pieces(self, piece_class, positions, colour):
        """Helper method to place multiple pieces on the board."""
        for pos in positions:
            self._add_piece(piece_class, pos, colour)

    def update_piece_move_list(self):
        threats = self.is_check(self.turn)
        BOARD_ALLOWED_MOVES = []
        if threats:
            king_position = self.find_king(self.turn)
            for threat in threats:
                BOARD_ALLOWED_MOVES.append(threat.position)
                BOARD_ALLOWED_MOVES += get_positions_between(threat.position, king_position)

        # Need to update current turns moveset first
        for piece in self.pieces:
            if piece.colour == self.turn:
                piece._update_moves(self.board, BOARD_ALLOWED_MOVES)

        # Then we update next turns moveset
        for piece in self.pieces:
            if piece.colour != self.turn:
                piece._update_moves(self.board, [])

    def setup_board(self):
        """Sets up the initial board with all pieces in their starting positions."""
        # Place pawns
        self._place_pieces(Pawn, [(1, i) for i in range(8)], Colour.BLACK)
        self._place_pieces(Pawn, [(6, i) for i in range(8)], Colour.WHITE)

        # Place other pieces
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
        self.update_piece_move_list()

    def move_piece(self, piece, new_position):
        """Attempts to move a piece and handles check validation."""
        if not is_in_bounds(*new_position):
            print("Invalid move: Out of bounds")
            return
        if not self.is_valid_move(piece, new_position):
            print("Invalid move: Move not allowed for piece")
            return

        # Simulate move to check for threats
        old_position = piece.position
        current_piece = self._simulate_move(piece, new_position)

        if self.is_check(self.turn):
            print("Invalid move: Leaves game in check")
            self._revert_move(piece, new_position, old_position, current_piece)
            return

        # Execute the move and switch turns
        self._finalize_move(piece, old_position, new_position)
        self.pieces = [p for row in self.board for p in row if p is not None]

    def _simulate_move(self, piece, new_position):
        """Simulates moving a piece and returns the piece at the new position."""
        old_position = piece.position
        current_piece = self.board[new_position[0]][new_position[1]]
        self.board[old_position[0]][old_position[1]] = None
        self.board[new_position[0]][new_position[1]] = piece
        piece.position = new_position
        self.update_piece_move_list()
        return current_piece

    def _revert_move(self, piece, new_position, old_position, current_piece):
        """Reverts a simulated move."""
        piece.position = old_position
        self.board[old_position[0]][old_position[1]] = piece
        self.board[new_position[0]][new_position[1]] = current_piece
        self.update_piece_move_list()

    def _finalize_move(self, piece, old_position, new_position):
        """Finalizes a valid move and switches the turn."""
        # self.board[old_position[0]][old_position[1]] = None
        # self.board[new_position[0]][new_position[1]] = piece
        piece.has_moved = True
        self.turn = Colour.WHITE if self.turn == Colour.BLACK else Colour.BLACK

    def render(self, screen):
        """Renders the board and all active pieces."""
        screen.blit(self.sprite, dest=(0, 0))

        for piece in self.pieces:
            if piece == self.selected_piece:
                continue

            piece_x, piece_y = self.get_render_position(piece.position)
            piece.render(screen, (piece_x, piece_y))

    def get_render_position(self, position: tuple[int, int]):
        """Calculates the screen position for a piece."""
        piece_x = self.board_start_x + (position[0] * self.square_size_x) - (self.square_size_x * 0.1)
        piece_y = self.board_start_y + (position[1] * self.square_size_y) + (self.square_size_y * 0.25)
        return piece_x, piece_y

    def get_piece_at(self, mouse_x, mouse_y):
        """Gets the piece at a specific mouse position on the board."""
        board_x = (mouse_x - self.board_start_x) // self.square_size_x
        board_y = (mouse_y - self.board_start_y) // self.square_size_y

        if is_in_bounds(board_x, board_y):
            return self.board[int(board_x)][int(board_y)]

    @staticmethod
    def is_valid_move(piece, position):
        """Checks if a move is valid for a given piece."""
        return position in piece.move_list

    def find_king(self, colour):
        """Finds the position of the king for a given colour."""
        for row in self.board:
            for piece in row:
                if isinstance(piece, King) and piece.colour == colour:
                    return piece.position
        return None

    def is_check(self, colour: Colour) -> list:
        """Checks if the given colour's king is in check."""
        threats = []
        king_position = self.find_king(colour)
        if king_position is None:
            return threats

        for row in self.board:
            for piece in row:
                if piece and piece.colour != colour and piece.can_attack(self.board, king_position):
                    threats.append(piece)
        return threats

    def can_capture(self, attacker):
        """Checks if any piece can capture the given attacker."""
        for row in self.board:
            for piece in row:
                if piece and piece.colour != attacker.colour and attacker.position in piece.move_list:
                    return True
        return False

    def can_block(self, attacker, king):
        """Checks if any piece can block the attacker from reaching the king."""
        if isinstance(attacker, (Rook, Bishop, Queen)):
            positions_to_block = self.get_positions_between(attacker.position, king.position)
            for row in self.board:
                for piece in row:
                    if piece and piece.colour == king.colour:
                        if any(move in positions_to_block for move in piece.move_list):
                            return True
        return False

    def is_checkmate(self) -> bool:
        """Checks if the current player is in checkmate."""
        attacking_pieces = self.is_check(self.turn)
        if not attacking_pieces:
            return False

        king_position = self.find_king(self.turn)
        king_piece = self.board[king_position[0]][king_position[1]]

        if king_piece.move_list:
            return False

        for attacker in attacking_pieces:
            if self.can_capture(attacker) or self.can_block(attacker, king_piece):
                return False

        return True

    @staticmethod
    def get_positions_between(start, end):
        """Returns all positions between two points on the board."""
        positions = []
        row_step = (end[0] - start[0]) // max(1, abs(end[0] - start[0]))
        col_step = (end[1] - start[1]) // max(1, abs(end[1] - start[1]))

        current_row, current_col = start[0] + row_step, start[1] + col_step
        while (current_row, current_col) != end:
            positions.append((current_row, current_col))
            current_row += row_step
            current_col += col_step

        return positions

    def is_game_over(self) -> bool:
        """Checks if the game is over due to checkmate or stalemate."""
        return self.is_stalemate() or self.is_checkmate()

    @staticmethod
    def is_stalemate() -> bool:
        """Checks if the game is in a stalemate state."""
        return False
