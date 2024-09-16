import pygame
from .abc_game_state import GameState
from .board import Board

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class SingleGameState(GameState):
    def __init__(self, screen):
        super().__init__(screen)
        self.board = Board(WIDTH, HEIGHT)
        self.selected_piece = None
        self.mouse_offset = (0, 0)

    @staticmethod
    def get_mouse_coords():
        """
        Returns mouse coordinates (row, column), rearranged to match chess board orientation.
        :return: Tuple (row, column)
        """
        return pygame.mouse.get_pos()[::-1]

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()[::-1]  # Reverse for chess orientation
            piece = self.board.get_piece_at(mouse_x, mouse_y)

            if piece:
                if piece.colour != self.board.turn:
                    print("Not your turn")
                    return
                if not piece.move_list:
                    print("No valid moves im afraid")
                    return
                self.board.selected_piece = piece
                self.selected_piece = piece

                piece_x, piece_y = piece.position
                piece_x = self.board.board_start_x + (piece_x * self.board.square_size_x) - (
                        self.board.square_size_x * 0.1)
                piece_y = self.board.board_start_y + (piece_y * self.board.square_size_y) + (
                        self.board.square_size_y * 0.25)

                self.mouse_offset = (mouse_x - piece_x, mouse_y - piece_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.board.selected_piece:
                mouse_x, mouse_y = pygame.mouse.get_pos()[::-1]
                new_x = int((mouse_x - self.board.board_start_x) // self.board.square_size_x)
                new_y = int((mouse_y - self.board.board_start_y) // self.board.square_size_y)
                self.board.move_piece(self.selected_piece, (new_x, new_y))
                self.board.selected_piece = None

        if self.board.is_game_over():
            return "GAMEOVER"

    def update(self):
        if self.board.is_game_over():
            return "GAMEOVER"  # Switch to game over state
        return None

    def render(self):
        self.board.render(self.screen)
        if self.board.selected_piece:
            mouse_x, mouse_y = self.get_mouse_coords()

            adjusted_x = mouse_x - self.mouse_offset[0]
            adjusted_y = mouse_y - self.mouse_offset[1]

            self.board.selected_piece.render(self.screen, (adjusted_x, adjusted_y))
