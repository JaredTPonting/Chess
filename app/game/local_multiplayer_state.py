from .abc_game_state import GameState

import pygame

from .board import Board

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class LocalState(GameState):
    def __init__(self, screen):
        super().__init__(screen)
        self.board = Board(WIDTH, HEIGHT)
        self.selected_piece = None
        self.mouse_offset = (0, 0)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()[::-1]  # Reverse for chess orientation
            piece = self.board.get_piece_at(mouse_x, mouse_y)

            if piece:
                if piece.colour != self.board.turn:
                    print("Not your turn")
                    return
                self.board.selected_piece = piece
                self.selected_piece = piece

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.board.selected_piece:
                mouse_x, mouse_y = pygame.mouse.get_pos()[::-1]
                new_x = int((mouse_x - self.board.board_start_x) // self.board.square_size_x)
                new_y = int((mouse_y - self.board.board_start_y) // self.board.square_size_y)
                self.board.move_piece(self.selected_piece, (new_x, new_y))
                self.board.selected_piece = None

    def update(self):
        if self.board.is_game_over():
            return "GAMEOVER"  # Switch to game over state
        return None

    def render(self):
        self.board.render(self.screen)
