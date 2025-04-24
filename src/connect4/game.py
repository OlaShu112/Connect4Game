import numpy as np

class Connect4Game:
    ROWS = 6
    COLS = 7
    EMPTY = 0

    def __init__(self):
        self.board = np.zeros((self.ROWS, self.COLS), dtype=int)
        self.current_player = 1
        self.game_over = False

    def reset(self):
        """Resets the game board and status."""
        self.board = np.zeros((self.ROWS, self.COLS), dtype=int)
        self.current_player = 1
        self.game_over = False

    def make_move(self, col):
        """
        Makes a move in the given column for the current player.
        Returns True if move is successful, otherwise False.
        """
        if not self.is_valid_move(col):
            return False

        row = self.get_next_open_row(col)
        self.board[row][col] = self.current_player
        if self.check_winner(row, col):
            self.game_over = True
        self.current_player = 3 - self.current_player  # Switch player
        return True

    def is_valid_move(self, col):
        """Checks if the column can accept another piece."""
        return self.board[0][col] == self.EMPTY

    def get_next_open_row(self, col):
        """Finds the next open row in a column."""
        for row in range(self.ROWS-1, -1, -1):
            if self.board[row][col] == self.EMPTY:
                return row
        return -1

    def get_valid_moves(self):
        """Returns a list of valid column indices."""
        return [col for col in range(self.COLS) if self.is_valid_move(col)]

    def check_winner(self, row, col):
        """Checks whether the current move resulted in a win."""
        piece = self.board[row][col]

        def count_direction(dx, dy):
            count = 0
            r, c = row + dy, col + dx
            while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r][c] == piece:
                count += 1
                r += dy
                c += dx
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonals
        for dx, dy in directions:
            count = 1 + count_direction(dx, dy) + count_direction(-dx, -dy)
            if count >= 4:
                return True
        return False

    def is_draw(self):
        """Checks if the game is a draw."""
        return not self.game_over and all(self.board[0][col] != self.EMPTY for col in range(self.COLS))

    def get_board_copy(self):
        """Returns a deep copy of the board (useful for AI simulations)."""
        return np.copy(self.board)

    def get_current_player(self):
        """Returns the current player's number (1 or 2)."""
        return self.current_player
