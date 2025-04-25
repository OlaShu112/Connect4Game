import numpy as np

class GameState:
    def __init__(self, board: np.ndarray, player_id: int):
        self.board = board.copy()
        self.player_id = player_id

    def get_valid_moves(self):
        return [c for c in range(self.board.shape[1]) if self.board[0][c] == 0]

    def make_move(self, col, player):
        for row in reversed(range(self.board.shape[0])):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                break

    def undo_move(self, col):
        for row in range(self.board.shape[0]):
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                break

    def is_terminal_node(self):
        return self.check_win(self.player_id) or self.check_win(3 - self.player_id) or all(self.board[0] != 0)

    def evaluate(self, player_id):
        if self.check_win(player_id):
            return 1000
        elif self.check_win(3 - player_id):
            return -1000
        else:
            return 0

    def check_win(self, player):
        for c in range(self.board.shape[1] - 3):
            for r in range(self.board.shape[0]):
                if all(self.board[r][c+i] == player for i in range(4)):
                    return True
        for c in range(self.board.shape[1]):
            for r in range(self.board.shape[0] - 3):
                if all(self.board[r+i][c] == player for i in range(4)):
                    return True
        for c in range(self.board.shape[1] - 3):
            for r in range(self.board.shape[0] - 3):
                if all(self.board[r+i][c+i] == player for i in range(4)):
                    return True
        for c in range(self.board.shape[1] - 3):
            for r in range(3, self.board.shape[0]):
                if all(self.board[r-i][c+i] == player for i in range(4)):
                    return True
        return False
