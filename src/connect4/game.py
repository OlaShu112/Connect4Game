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
        self.board = np.zeros((self.ROWS, self.COLS), dtype=int)
        self.current_player = 1
        self.game_over = False

    def is_game_over(self):
        return self.game_over

    def make_move(self, col):
        if not self.is_valid_move(col):
            return -1  # Some safe error value

        row = self.get_next_open_row(col)
        self.board[row][col] = self.current_player
        if self.check_winner(row, col):
            self.game_over = True
        self.current_player = 3 - self.current_player  # Switch player
        return row  # return the row


    def is_valid_move(self, col):
        return self.board[0][col] == self.EMPTY

    def get_next_open_row(self, col):
        for row in range(self.ROWS-1, -1, -1):
            if self.board[row][col] == self.EMPTY:
                return row
        return -1

    def get_valid_moves(self):
        return [col for col in range(self.COLS) if self.is_valid_move(col)]

    def check_winner(self, row, col):
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
        return not self.game_over and all(self.board[0][col] != self.EMPTY for col in range(self.COLS))

    def get_board_copy(self):
        return np.copy(self.board)

    def get_current_player(self):
        return self.current_player
