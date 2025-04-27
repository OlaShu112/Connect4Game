import numpy as np
from connect4.constants import ROW_COUNT, COLUMN_COUNT

def create_board():
    """Creates and returns an empty Connect 4 board."""
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def drop_piece(board, col, player):
    """Drops a player's piece into a column."""
    for row in reversed(range(ROW_COUNT)):
        if board[row][col] == 0:
            board[row][col] = player
            return row
    return -1

def valid_move(board, col):
    return board[0][col] == 0

def switch_turn(turn):
    return 2 if turn == 1 else 1

def check_win(board, player):
    # Horizontal check
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Vertical check
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Positive diagonal check
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Negative diagonal check
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    return False

def board_is_full(board):
    return not any(board[0][c] == 0 for c in range(COLUMN_COUNT))

def block_player_move(board, player):
    for col in range(len(board[0])):
        if valid_move(board, col):
            temp_board = [row.copy() for row in board]
            row = drop_piece(temp_board, col, player)
            if check_win(temp_board, player):
                return col
    return -1
