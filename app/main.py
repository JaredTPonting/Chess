import pygame
import sys
from game.board import Board

pygame.init()

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")


class GameState:
    def __init__(self, screen):
        self.screen = screen

    def handle_events(self, event):
        pass

    def update(self):
        pass

    def render(self):
        pass


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

            self.board.selected_piece.render(screen, (adjusted_x, adjusted_y))


class GameOverState(GameState):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.Font(None, 74)
        self.game_over_text = self.font.render("Game Over", True, WHITE)
        self.restart_text = self.font.render("Restart", True, WHITE)
        self.button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.button_rect.collidepoint(mouse_x, mouse_y):
                return "TITLE"  # Switch to title state
        return None

    def render(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.game_over_text, (WIDTH // 2 - 100, HEIGHT // 3))
        pygame.draw.rect(self.screen, WHITE, self.button_rect)
        self.screen.blit(self.restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 10))


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = TitleState(screen)

    def change_state(self, new_state):
        if new_state == "TITLE":
            self.state = TitleState(self.screen)
        elif new_state == "SINGLEGAME":
            self.state = SingleGameState(self.screen)
        elif new_state == "GAMEOVER":
            self.state = GameOverState(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                new_state = self.state.handle_events(event)
                if new_state:
                    self.change_state(new_state)

            self.state.update()
            self.state.render()

            pygame.display.flip()


if __name__ == "__main__":
    game = Game(screen)
    game.run()
