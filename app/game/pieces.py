from typing import Union, List

from app import get_piece_asset_path

import pygame
import os


class Piece:
    def __init__(self, position, colour, sprite_path, square_size):
        self.position = position
        self.colour = colour
        self.has_moved = False
        self.square_size = square_size
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (square_size, square_size))

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

    def can_attack(self, board, target_position):
        """
        Checks whether piece can attack target position
        :param board:
        :param target_position: (x: int, y: int)
        :return:
        """
        return target_position in self.valid_moves(board)

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
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, 'Pawn')
        super().__init__(position, colour, sprite_path, square_size)
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

        # TODO: add enpassant to this method

        return moves

    def can_attack(self, board, target_position):
        # TODO: add enpassant to this method

        x, y = self.position
        tx, ty = target_position
        return (tx == x + self.direction and (ty == y + 1 or ty == y - 1) and board[tx][ty] is not None and board[tx][
            ty].colour != self.colour)


class Rook(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, 'Rook')
        super().__init__(position, colour, sprite_path, square_size)

    def valid_moves(self, board):
        moves = []
        x, y = self.position

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            new_x, new_y = x, y

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
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, "Knight")
        super().__init__(position, colour, sprite_path, square_size)

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
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, "Bishop")
        super().__init__(position, colour, sprite_path, square_size)

    def valid_moves(self, board):
        moves = []
        x, y = self.position

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            new_x, new_y = x, y

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

        # if not self.has_moved:

        return moves


class Queen(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, "Queen")
        super().__init__(position, colour, sprite_path, square_size)

    def valid_moves(self, board):
        moves = []
        x, y = self.position

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            new_x, new_y = x, y

            while True:
                new_x += dx
                new_y += dy

                if not self.is_in_bounds(new_x, new_y):
                    break

                if board[new_x][new_y] is None and not self.in_check():
                    moves.append((new_x, new_y))
                elif board[new_x][new_y].colour != self.colour and not self.in_check():
                    moves.append((new_x, new_y))
                    break
                else:
                    break

        return moves


class King(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, "King")
        super().__init__(position, colour, sprite_path, square_size)

    def position_is_check(self, board, new_position):
        for row in board:
            for piece in row:
                if piece is not None and piece.colour != self.colour:
                    if piece.can_attack(board, new_position):
                        return True

        return False

    def valid_moves(self, board):
        moves = []
        x, y = self.position

        steps = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in steps:
            new_x = x + dx
            new_y = y + dy

            if (not self.is_in_bounds(new_x, new_y)) or self.position_is_check(board, (new_x, new_y)):
                continue
            elif board[new_x][new_y].colour != self.colour or board[new_x][new_y] is None:
                moves.append((new_x, new_y))

        # TODO: add castling functionality

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
