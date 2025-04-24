from typing import List


class SmartAgent:
    """
    SmartAgent for Connect 4.
    
    This agent uses simple yet effective heuristics to make decisions:
        1. Select a winning move if available.
        2. Block the opponent's winning move.
        3. Prioritize the center column.
        4. Fall back to the first valid move.

    Attributes:
        player_id (int): The ID representing this agent (usually 1 or 2).
        name (str): The display name of the agent.
    """

    def __init__(self, player_id: int, name: str = "SmartAgent") -> None:
        """
        Initializes the SmartAgent instance.

        Args:
            player_id (int): The ID assigned to this agent (1 or 2).
            name (str): The agent's name (default: 'SmartAgent').
        """
        self.player_id = player_id
        self.name = name

    def get_move(self, game) -> int:
        """
        Determines the best column to play based on simple heuristics.

        Args:
            game: The game instance which must implement:
                - get_valid_moves() -> List[int]
                - is_winning_move(column: int, player_id: int) -> bool
                - columns (int): Total number of columns in the board

        Returns:
            int: The selected column index.

        Raises:
            ValueError: If there are no valid moves available.
        """
        valid_moves: List[int] = game.get_valid_moves()
        if not valid_moves:
            raise ValueError(f"[{self.name}] No valid moves available.")

        # Step 1: Take the winning move if available
        for col in valid_moves:
            if game.is_winning_move(col, self.player_id):
                return col

        # Step 2: Block the opponent's winning move
        opponent_id = 2 if self.player_id == 1 else 1
        for col in valid_moves:
            if game.is_winning_move(col, opponent_id):
                return col

        # Step 3: Prefer the center column if available
        center_column = game.columns // 2
        if center_column in valid_moves:
            return center_column

        # Step 4: Fallback - choose the first valid move
        return valid_moves[0]

    def __str__(self) -> str:
        """
        Returns the name of the agent for easy identification.
        """
        return self.name
