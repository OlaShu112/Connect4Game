from typing import List, Optional, Tuple


class MinimaxAgent:
    """
    MinimaxAgent for Connect 4.

    This agent uses the Minimax algorithm with alpha-beta pruning to evaluate the best possible move
    based on a specified search depth.

    Attributes:
        player_id (int): The ID representing this agent (1 or 2).
        name (str): Agent's display name.
        max_depth (int): Depth to which the game tree is evaluated.
    """

    def __init__(self, player_id: int, max_depth: int = 4, name: str = "MinimaxAgent") -> None:
        """
        Initializes the MinimaxAgent instance.

        Args:
            player_id (int): The agent's ID (1 or 2).
            max_depth (int): Search depth for Minimax.
            name (str): Optional name of the agent.
        """
        self.player_id = player_id
        self.max_depth = max_depth
        self.name = name

    def get_move(self, game) -> int:
        """
        Selects the best move using the Minimax algorithm with alpha-beta pruning.

        Args:
            game: The current GameState instance.

        Returns:
            int: Best column index to play.
        """
        best_score = float("-inf")
        best_col = None

        for col in game.get_valid_moves():
            game.make_move(col, self.player_id)
            score = self.minimax(game, self.max_depth - 1, False, float("-inf"), float("inf"))
            game.undo_move(col)

            if score > best_score:
                best_score = score
                best_col = col

        if best_col is None:
            raise ValueError(f"[{self.name}] No valid move found.")
        return best_col

    def minimax(
        self,
        game,
        depth: int,
        maximizing_player: bool,
        alpha: float,
        beta: float
    ) -> int:
        """
        Recursive implementation of the Minimax algorithm with alpha-beta pruning.

        Args:
            game: The current GameState instance.
            depth (int): Remaining depth to evaluate.
            maximizing_player (bool): Whether the current layer is maximizing.
            alpha (float): Alpha value for pruning.
            beta (float): Beta value for pruning.

        Returns:
            int: Evaluation score of the game state.
        """
        if depth == 0 or game.is_terminal_node():
            return game.evaluate(self.player_id)

        current_player = self.player_id if maximizing_player else (2 if self.player_id == 1 else 1)

        if maximizing_player:
            max_eval = float("-inf")
            for col in game.get_valid_moves():
                game.make_move(col, current_player)
                score = self.minimax(game, depth - 1, False, alpha, beta)
                game.undo_move(col)
                max_eval = max(max_eval, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for col in game.get_valid_moves():
                game.make_move(col, current_player)
                score = self.minimax(game, depth - 1, True, alpha, beta)
                game.undo_move(col)
                min_eval = min(min_eval, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_eval

    def __str__(self) -> str:
        return self.name
