import pygame
import sys

from app.game.game_over_state import GameOverState
from app.game.local_multiplayer_state import SingleGameState
from app.game.title_state import TitleState
from game.board import Board

pygame.init()

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")













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
