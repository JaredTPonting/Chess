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


def get_mouse_coords():
    """
    get mouse coords but switch position to make similar to how we define chess board
    :return: (X, Y) equivelant to (ROW direction, COLUMN direction)
    """
    column_dir, row_dir = pygame.mouse.get_pos()
    return (row_dir, column_dir)


def main():
    game_board = Board(WIDTH, HEIGHT)
    mouse_offset = (0, 0)
    selected_piece = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse Click event to pick up the piece
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = get_mouse_coords()
                piece = game_board.get_piece_at(mouse_x, mouse_y)

                if piece:
                    if piece.colour != game_board.turn:
                        continue
                    game_board.selected_piece = piece
                    selected_piece = piece

                    piece_x, piece_y = piece.position

                    # Adjust position to fit within board (excluding boarder)
                    piece_x = game_board.board_start_x + (piece_x * game_board.square_size_x) - (
                            game_board.square_size_x * 0.1)
                    piece_y = game_board.board_start_y + (piece_y * game_board.square_size_y) + (
                            game_board.square_size_y * 0.25)

                    mouse_offset = (mouse_x - piece_x, mouse_y - piece_y)

            # Mouse release event to drop the piece
            elif event.type == pygame.MOUSEBUTTONUP:
                if game_board.selected_piece:
                    mouse_x, mouse_y = get_mouse_coords()

                    new_x = int((mouse_x - game_board.board_start_x) // game_board.square_size_x)
                    new_y = int((mouse_y - game_board.board_start_y) // game_board.square_size_y)

                    if game_board.is_in_bounds(new_x, new_y) and game_board.is_valid_move(game_board.selected_piece,
                                                                                          (new_x, new_y)):
                        game_board.move_piece(piece, (new_x, new_y))

                    game_board.selected_piece = None

        # Render Board and Pieces
        draw_board(game_board, screen)

        # If piece being dragged, Render it last
        if game_board.selected_piece:
            mouse_x, mouse_y = get_mouse_coords()

            adjusted_x = mouse_x - mouse_offset[0]
            adjusted_y = mouse_y - mouse_offset[1]

            selected_piece.render(screen, (adjusted_x, adjusted_y))
        pygame.display.flip()


if __name__ == "__main__":
    main()
