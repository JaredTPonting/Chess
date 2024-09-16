from typing import List, Union

import pygame
import copy

from app import get_board_asset_path
from app.game.pieces.King import King
from app.game.pieces.Queen import Queen
from app.game.pieces.Bishop import Bishop
from app.game.pieces.Knight import Knight
from app.game.pieces.Rook import Rook
from app.game.pieces.Pawn import Pawn
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
        self.board: {tuple[int, int]: Union[King, Queen, Bishop, Knight, Rook, Pawn]} = {}
        self.turn = Colour.WHITE
        self.selected_piece = None
        self.check = False
        self.stalemate = False
        self.checkmate = False
        self.en_passant_target = None

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
        self.board[position] = piece

    def _place_pieces(self, piece_class, positions, colour):
        """Helper method to place multiple pieces on the board."""
        for pos in positions:
            self._add_piece(piece_class, pos, colour)

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

    def update_piece_move_list(self, colour=None):
        if colour is None:
            colour = self.turn
        threats = self.is_check(colour)
        BOARD_ALLOWED_MOVES = []
        if threats:
            king_position = self.find_king(colour)
            for threat in threats:
                BOARD_ALLOWED_MOVES.append(threat.position)
                BOARD_ALLOWED_MOVES += get_positions_between(threat.position, king_position)

        # Need to update current turns moveset first
        for piece in self.board.values():
            if piece.colour == colour:
                piece.update_moves(self, BOARD_ALLOWED_MOVES)

        # Then we update next turns moveset
        for piece in self.board.values():
            if piece.colour != colour:
                piece.update_moves(self, [])

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

        # Check for promotion if the piece is a Pawn and reached the promotion rank
        if isinstance(piece, Pawn):
            promotion_rank = 0 if piece.colour == Colour.WHITE else 7
            if new_position[0] == promotion_rank:
                self.promote_pawn(piece, new_position)

        # Execute the move and switch turns
        self._finalize_move(piece)
        self.is_checkmate()

        if isinstance(piece, Pawn) and abs(new_position[0] - piece.position[0]) == 2:
            # If the pawn moved two squares forward, set the en passant target to the square behind it
            self.en_passant_target = (new_position[0] - piece.direction, new_position[1])
        else:
            # Reset the en passant target if no two-square move happened
            self.en_passant_target = None

    def promote_pawn(self, pawn, position):
        """Promotes a pawn to another piece when it reaches the last rank."""
        print(f"Pawn at {position} is being promoted!")

        # Ask the user for promotion choice (can be expanded to a GUI later)
        promotion_choice = input("Choose piece for promotion (Q=Queen, R=Rook, B=Bishop, K=Knight): ").upper()

        if promotion_choice == 'Q':
            new_piece = Queen(position=position, colour=pawn.colour, square_size=self.square_size_x)
        elif promotion_choice == 'R':
            new_piece = Rook(position=position, colour=pawn.colour, square_size=self.square_size_x)
        elif promotion_choice == 'B':
            new_piece = Bishop(position=position, colour=pawn.colour, square_size=self.square_size_x)
        elif promotion_choice == 'K':
            new_piece = Knight(position=position, colour=pawn.colour, square_size=self.square_size_x)
        else:
            print("Invalid choice! Defaulting to Queen.")
            new_piece = Queen(position=position, colour=pawn.colour, square_size=self.square_size_x)

        # Replace the pawn with the promoted piece
        self.board[position] = new_piece
        print(f"Pawn promoted to {new_piece.__class__.__name__}")

    def _simulate_move(self, piece, new_position, colour=None):
        """Simulates moving a piece and returns the piece at the new position."""
        if colour is None:
            colour = self.turn
        old_position = piece.position
        if new_position in self.board.keys():
            current_piece = self.board[new_position]
        else:
            current_piece = None

        # if self.en_passant_target == new_position and isinstance(piece, Pawn):

        self.board.pop(old_position)
        self.board[new_position] = piece
        piece.position = new_position
        self.update_piece_move_list(colour)
        return current_piece

    def _revert_move(self, piece, new_position, old_position, current_piece, colour=None):
        """Reverts a simulated move."""
        if colour is None:
            colour = self.turn
        piece.position = old_position
        self.board[old_position] = piece
        if current_piece is not None:
            self.board[new_position] = current_piece
        else:
            self.board.pop(new_position)
        self.update_piece_move_list(colour)

    def _finalize_move(self, piece):
        """Finalizes a valid move and switches the turn."""
        piece.has_moved = True
        self.turn = Colour.WHITE if self.turn == Colour.BLACK else Colour.BLACK

    def render(self, screen):
        """Renders the board and all active pieces."""
        screen.blit(self.sprite, dest=(0, 0))

        for piece in self.board.values():
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
            return self.board[(board_x, board_y)]

    @staticmethod
    def is_valid_move(piece, position):
        """Checks if a move is valid for a given piece."""
        return position in piece.move_list

    def find_king(self, colour):
        """Finds the position of the king for a given colour."""
        for i, v in self.board.items():
            if isinstance(v, King) and v.colour.value == colour.value:
                return i
        return None

    def is_check(self, colour: Colour) -> list:
        """Checks if the given colour's king is in check."""
        threats = []
        king_position = self.find_king(colour)
        if king_position is None:
            return threats

        for i, v in self.board.items():
            if v and v.colour != colour and v.can_attack(self.board, king_position):
                threats.append(v)
        return threats

    def can_capture(self, attacker):
        """Checks if any piece can capture the given attacker.
            Used only to check for check
        """
        for i, piece in self.board.items():
            if piece and piece.colour != attacker.colour and attacker.position in piece.move_list:
                return True
        return False

    def can_block(self, attacker, king):
        """Checks if any piece can block the attacker from reaching the king."""
        if isinstance(attacker, (Rook, Bishop, Queen)):
            positions_to_block = self.get_positions_between(attacker.position, king.position)
            for i, piece in self.board.items():
                if piece and piece.colour == king.colour:
                    if any(move in positions_to_block for move in piece.move_list):
                        return True
        return False

    def is_checkmate(self):
        """Checks if the current player is in checkmate."""
        attacking_pieces = self.is_check(self.turn)
        if not attacking_pieces:
            self.checkmate = False
            return

        king_position = self.find_king(self.turn)
        king_piece = self.board[king_position]

        other_colour = Colour.WHITE if self.turn == Colour.BLACK else Colour.BLACK

        if king_piece.move_list:
            new_move_list = []
            for move in king_piece.move_list:
                kings_capture = self._simulate_move(king_piece, move, other_colour)
                threats = self.is_check(self.turn)
                if not threats:
                    new_move_list.append(move)
                self._revert_move(king_piece, move, king_position, kings_capture, other_colour)

            if new_move_list:
                self.checkmate = False
                return
            self.checkmate = True
            return

        for attacker in attacking_pieces:
            if self.can_capture(attacker) or self.can_block(attacker, king_piece):
                self.checkmate = False

        self.checkmate = True

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
        return self.stalemate or self.checkmate

    def is_stalemate(self):
        """Checks if the game is in a stalemate state."""
        self.stalemate = False
