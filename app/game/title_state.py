from .abc_game_state import GameState

import pygame

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class TitleState(GameState):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.Font(None, 74)
        self.title_text = self.font.render("Chess", True, WHITE)
        self.new_game_text = self.font.render("New Game", True, WHITE)
        self.button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 400, 75)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.button_rect.collidepoint(mouse_x, mouse_y):
                return "SINGLEGAME"  # Switch to game state
        return None

    def render(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.title_text, (WIDTH // 2 - 100, HEIGHT // 3))
        pygame.draw.rect(self.screen, (100, 100, 100), self.button_rect)
        self.screen.blit(self.new_game_text, (WIDTH // 2 - 100, HEIGHT // 2 + 10))
