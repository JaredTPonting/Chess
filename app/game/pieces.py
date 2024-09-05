from typing import Union, List

from app import get_piece_asset_path

import pygame
import os


class Piece:
    def __init__(self, position, colour, sprite_path, square_size):
        self.actual_y = None
        self.actual_x = None
        self.position = position
        self.colour = colour
        self.has_moved = False
        self.square_size = square_size
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (0.5 * square_size, square_size))

    def render(self, screen, position):
        piece_x, piece_y = position
        self.actual_x = position[0]
        self.actual_y = position[1]
        screen.blit(self.sprite, (piece_y, piece_x))

    def move(self, new_position):
        self.position = new_position
        self.has_moved = True

    def valid_moves(self, board):
        """
        Checks board for all valid moves for current piece
        :param board:
        :return: (List[(ROW, COL)]) List of all valid moves (ROW: int, COL: int)
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
        return 0 <= x < 8 and 0 <= y < 8


class Pawn(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, 'Pawn')
        super().__init__(position, colour, sprite_path, square_size)
        self.direction = 1 if self.colour == "BLACK" else -1

    def valid_moves(self, board: List[List[Union[Piece, None]]]) -> List[tuple]:
        moves = []
        ROW, COL = self.position

        # Move PAWN one square forward
        next_ROW = ROW + self.direction
        if self.is_in_bounds(next_ROW, COL) and board[next_ROW][COL] is None:
            moves.append((next_ROW, COL))

        # First move only. Move PAWN two squares forward
        if not self.has_moved:
            next_2_ROW = next_ROW + self.direction
            if self.is_in_bounds(next_2_ROW, COL) and board[next_2_ROW][COL] is None:
                moves.append((next_2_ROW, COL))

        # Capture Moves
        for dcol in [-1, 1]:
            next_COL = COL + dcol
            if self.is_in_bounds(next_ROW, next_COL) and board[next_ROW][next_COL] is not None:
                if board[next_ROW][next_COL].colour != self.colour:
                    moves.append((next_ROW, next_COL))

        # TODO: add enpassant to this method

        return moves

    def can_attack(self, board, target_position):
        # TODO: add enpassant to this method

        ROW, COL = self.position
        trow, tcol = target_position
        return (trow == ROW + self.direction and (tcol == COL + 1 or tcol == COL - 1) and board[trow][tcol] is not None and board[trow][
            tcol].colour != self.colour)


class Rook(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, 'Rook')
        super().__init__(position, colour, sprite_path, square_size)

    def valid_moves(self, board):
        moves = []
        ROW, COL = self.position

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for drow, dcol in directions:
            new_row, new_col = ROW, COL

            while True:
                new_row += drow
                new_col += dcol

                if not self.is_in_bounds(new_row, new_col):
                    break

                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board[new_row][new_col].colour != self.colour:
                    moves.append((new_row, new_col))
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
        ROW, COL = self.position
        jumps = [(2, -1), (2, 1), (-2, -1), (-2, 1), (1, 2), (-1, 2), (1, -2), (-1, -2)]

        for drow, dcol in jumps:
            new_row = ROW + drow
            new_col = COL + dcol

            if not self.is_in_bounds(new_row, new_col):
                continue
            elif board[new_row][new_col] is None:
                moves.append((new_row, new_col))
            elif board[new_row][new_col].colour != self.colour:
                moves.append((new_row, new_col))

        return moves


class Bishop(Piece):
    def __init__(self, position, colour, square_size):
        sprite_path = get_piece_asset_path(colour, "Bishop")
        super().__init__(position, colour, sprite_path, square_size)

    def valid_moves(self, board):
        moves = []
        ROW, COL = self.position

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for drow, dcol in directions:
            new_row, new_col = ROW, COL

            while True:
                new_row += drow
                new_col += dcol

                if not self.is_in_bounds(new_row, new_col):
                    break

                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board[new_row][new_col].colour != self.colour:
                    moves.append((new_row, new_col))
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
        ROW, COL = self.position

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]

        for drow, dcol in directions:
            new_row, new_col = ROW, COL

            while True:
                new_row += drow
                new_col += dcol

                if not self.is_in_bounds(new_row, new_col):
                    break

                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board[new_row][new_col].colour != self.colour:
                    moves.append((new_row, new_col))
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
        ROW, COL = self.position

        steps = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]

        for drow, dcol in steps:
            new_row = ROW + drow
            new_col = COL + dcol

            if (not self.is_in_bounds(new_row, new_col)) or self.position_is_check(board, (new_row, new_col)):
                continue
            elif board[new_row][new_col].colour != self.colour or board[new_row][new_col] is None:
                moves.append((new_row, new_col))

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
