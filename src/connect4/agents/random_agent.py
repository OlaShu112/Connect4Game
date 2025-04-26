import random
from typing import List
import numpy as np  # <- optional if type hinting

class RandomAgent:
    def __init__(self, player_id: int = 2, name: str = "RandomAgent") -> None:
        """
        Initializes the RandomAgent with a player ID and an optional name.
        """
        self.player_id = player_id
        self.name = name

    def get_move(self, board: np.ndarray) -> int:
        """
        Selects a random valid column from the board (numpy array).

        Args:
            board (np.ndarray): The current board state.

        Returns:
           int: The selected column index.
        """
        valid_moves: List[int] = [c for c in range(board.shape[1]) if board[0][c] == 0]
        if not valid_moves:
            raise ValueError(f"[{self.name}] No valid moves available.")

        selected_move: int = random.choice(valid_moves)
        return selected_move

    def __str__(self) -> str:
        return self.name
