import pygame
import sys
from game.board import Board

pygame.init()

WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")


def draw_board(board, screen):
    board.render(screen)


def main():
    game_board = Board(WIDTH, HEIGHT)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board(game_board, screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
