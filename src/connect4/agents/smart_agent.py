import random
from typing import List
import numpy as np  # <- optional if you want better type hints

class SmartAgent:
    def __init__(self, player_id: int = 2, name: str = "SmartAgent") -> None:
        """
        Initializes the SmartAgent with a player ID and an optional name.
        """
        self.player_id = player_id
        self.name = name

    def get_move(self, board: np.ndarray) -> int:
        valid_moves: List[int] = [c for c in range(board.shape[1]) if board[0][c] == 0]
        opponent_id = 1 if self.player_id == 2 else 2

        # Try to win
        for col in valid_moves:
            temp_board = board.copy()
            for row in reversed(range(temp_board.shape[0])):
                if temp_board[row][col] == 0:
                    temp_board[row][col] = self.player_id
                    break
            if self.is_winning_move(temp_board, self.player_id):
                return col

        # Try to block opponent
        for col in valid_moves:
            temp_board = board.copy()
            for row in reversed(range(temp_board.shape[0])):
                if temp_board[row][col] == 0:
                    temp_board[row][col] = opponent_id
                    break
            if self.is_winning_move(temp_board, opponent_id):
                return col

        # Otherwise random
        return random.choice(valid_moves)

    def is_winning_move(self, board: np.ndarray, player_id: int) -> bool:
        rows, cols = board.shape

        # Horizontal
        for r in range(rows):
            for c in range(cols - 3):
                if all(board[r, c+i] == player_id for i in range(4)):
                    return True

        # Vertical
        for r in range(rows - 3):
            for c in range(cols):
                if all(board[r+i, c] == player_id for i in range(4)):
                    return True

        # Positive Diagonal
        for r in range(rows - 3):
            for c in range(cols - 3):
                if all(board[r+i, c+i] == player_id for i in range(4)):
                    return True

        # Negative Diagonal
        for r in range(3, rows):
            for c in range(cols - 3):
                if all(board[r-i, c+i] == player_id for i in range(4)):
                    return True

        return False

    def __str__(self) -> str:
        return self.name
