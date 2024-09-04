from typing import Union, List

from app import get_piece_asset_path

import pygame
import os


class Piece:
    def __init__(self, position, colour, sprite_path):
        self.position = position
        self.colour = colour
        self.sprite = pygame.image.load(sprite_path)
        self.has_moved = False

    def move(self, new_position):
        self.position = new_position
        self.has_moved = True

    def valid_moves(self, board):
        """
        Checks board for all valid moves for current piece
        :param board:
        :return: (List[(x, y)]) List of all valid moves (x: int, y: int)
        """
        raise NotImplementedError("This method should be overwritten in subclasses")

    @staticmethod
    def is_in_bounds(x: int, y: int) -> bool:
        """
        Checks whether the x, y position of move is within bounds of the board

        :param x: Potential X position of Piece
        :param y: Potential Y position of Piece
        :return:  (bool) True if position is in bounds
        """
        return 0 <= x <= 8 and 0 <= y <= 8


class Pawn(Piece):
    def __init__(self, position, colour):
        sprite_path = get_piece_asset_path(colour, 'Pawn')
        super().__init__(position, colour, sprite_path)
        self.direction = 1 if self.colour == "BLACK" else -1

    def valid_moves(self, board: List[List[Union[Piece, None]]]) -> List[tuple]:
        moves = []
        x, y = self.position

        # Move PAWN one square forward
        next_x = x + self.direction
        if self.is_in_bounds(next_x, y) and board[next_x][y] is None:
            moves.append((next_x, y))

        # First move only. Move PAWN two squares forward
        if not self.has_moved:
            next_2_x = next_x + self.direction
            if self.is_in_bounds(next_2_x, y) and board[next_2_x][y] is None:
                moves.append((next_2_x, y))

        # Capture Moves
        for dy in [-1, 1]:
            next_y = y + dy
            if self.is_in_bounds(next_x, next_y) and board[next_x][next_y] is not None:
                if board[next_x][next_y].colour != self.colour:
                    moves.append((next_x, next_y))

        # Add en passant.

        # PROMOTION WILL BE HANDLED WITHIN BOARD

        return moves


class Rook(Piece):
    def __init__(self, position, colour):
        sprite_path = get_piece_asset_path(colour, 'Rook')
        super().__init__(position, colour, sprite_path)

    def valid_moves(self, board):
        moves = []
        x, y = self.position

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        new_x, new_y = x, y
        for dx, dy in directions:

            while True:
                new_x += dx
                new_y += dy

                if not self.is_in_bounds(new_x, new_y):
                    break

                if board[new_x][new_y] is None:
                    moves.append((new_x, new_y))
                elif board[new_x][new_y].colour != self.colour:
                    moves.append((new_x, new_y))
                    break
                else:
                    break

        return moves


class Knight(Piece):
    def __init__(self, position, colour):
        sprite_path = get_piece_asset_path(colour, "Knight")
        super().__init__(position, colour, sprite_path)

    def valid_moves(self, board):
        moves = []
        x, y = self.position
        jumps = [(2, -1), (2, 1), (-2, -1), (-2, 1), (1, 2), (-1, 2), (1, -2), (-1, -2)]

        for dx, dy in jumps:
            new_x = x + dx
            new_y = y + dy

            if not self.is_in_bounds(new_x, new_y):
                continue
            elif board[new_x][new_y].colour != self.colour:
                moves.append((new_x, new_y))

        return moves


class Bishop(Piece):
    def __init__(self, position, colour):
        sprite_path = get_piece_asset_path(colour, "Bishop")
        super().__init__(position, colour, sprite_path)

    def valid_moves(self, board):
        moves = []
        x, y = self.position

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        new_x, new_y = x, y
        for dx, dy in directions:
            while True:
                new_x += dx
                new_y += dy

                if not self.is_in_bounds(new_x, new_y):
                    break

                if board[new_x][new_y] is None:
                    moves.append((new_x, new_y))
                elif board[new_x][new_y].colour != self.colour:
                    moves.append((new_x, new_y))
                    break
                else:
                    break
        return moves


if __name__ == "__main__":
    # Example of initializing Pygame and a pawn
    pygame.init()
    screen = pygame.display.set_mode((512, 512))  # Example window size

    white_pawn = Pawn((6, 4), 'white')
    white_pawn.valid_moves()

    # Blit the pawn's image onto the screen
    screen.blit(white_pawn.sprite, (64 * 4, 64 * 6))  # 4th file, 6th rank (0-indexed)

    pygame.display.flip()
