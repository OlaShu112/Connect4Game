class BaseAgent:
    def __init__(self, player_id: int, name: str = "BaseAgent") -> None:
        self.player_id = player_id
        self.name = name

    def get_move(self, board):
        raise NotImplementedError("Each agent must implement the get_move method.")
