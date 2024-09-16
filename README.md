# Python Chess Engine

## Overview

This project is a Python-based chess engine and game that supports most of the standard chess rules. The game includes all chess pieces (King, Queen, Rook, Bishop, Knight, Pawn) and supports legal moves, including checks and checkmates. The engine allows users to play a full game of chess and includes a graphical user interface (GUI) built using Pygame.

## Features

- Full chess game functionality
- Turn-based play with alternating white and black moves
- **Valid moves**: All standard chess moves (except castling and en passant and promoting pawns)
- **Check and checkmate** detection
- **Game states**: Check, checkmate
- Graphical representation of the board and pieces using Pygame

## Upcoming Features (To-Do)

- **Castling**: Implement king-side and queen-side castling
- **En passant**: Implement en passant pawn capture rules
- **Move validation**: More robust validation for special cases like draw by repetition
- **AI player**: Option for an AI opponent

## Installation

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/yourusername/chess-engine.git
    cd chess-engine
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate  # For Windows
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the chess game:
    ```bash
    python main.py
    ```

## How to Play

- The game will open a Pygame window where you can play chess using your mouse.
- Left-click to select a piece, and drag it to desired square.
- The game alternates between white and black turns, checking for legal moves.

## Game Rules Implemented

- **Standard moves** for all pieces (pawns, knights, bishops, rooks, queens, kings)
- **Checks and checkmates** are detected and enforced
- **Stalemate detection**

### Missing Features (WIP)

- **Castling**: Not yet implemented
- **En passant**: En passant capture has not been added yet

## Directory Structure

