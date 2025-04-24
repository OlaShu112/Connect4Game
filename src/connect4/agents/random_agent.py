import random
from typing import List

class RandomAgent:
    def __init__(self, player_id: int = 2, name: str = "RandomAgent") -> None:
        """
        Initializes the RandomAgent with a player ID and an optional name.

        Args:
            player_id (int): The ID of the player using this agent.
            name (str): The name of the agent. Defaults to "RandomAgent".
        """
        self.player_id = player_id
        self.name = name

    def get_move(self, game) -> int:
        """
        Selects a random valid column from the game state.

        Args:
            game: The game environment which must implement a `get_valid_moves()` method.

        Returns:
            int: The index of the selected column.

        Raises:
            ValueError: If there are no valid moves available.
        """
        valid_moves: List[int] = game.get_valid_moves()
        if not valid_moves:
            raise ValueError(f"[{self.name}] No valid moves available.")

        selected_move: int = random.choice(valid_moves)
        return selected_move

    def __str__(self) -> str:
        return self.name
