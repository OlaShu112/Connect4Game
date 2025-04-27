import numpy as np

class GameState:
    def __init__(self, board: np.ndarray, player_id: int): 
        """
        Initializes the GameState with the current board state and the active player.
        
        Args:
            board (np.ndarray): The game board.
            player_id (int): The current player (1 or 2).
        """
        self.board = board.copy()
        self.player_id = player_id

    def get_valid_moves(self):
        """
        Returns a list of columns where a move can still be made (i.e., not full).
        """
        return [c for c in range(self.board.shape[1]) if self.board[0][c] == 0]

    def make_move(self, col, player): 
        """
        Simulates dropping a piece into a column for a given player.
        
        Args:
            col (int): The column to drop the piece into.
            player (int): The ID of the player making the move.
        """
        for row in reversed(range(self.board.shape[0])):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                break

    def undo_move(self, col): 
        """
        Removes the top piece from the specified column (useful for Minimax backtracking).
        
        Args:
            col (int): The column to undo the move from.
        """
        for row in range(self.board.shape[0]):
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                break

    def is_terminal_node(self):
        """
        Checks if the game is over (either someone won or board is full).
        
        Returns:
            bool: True if game is over, False otherwise.
        """
        return self.check_win(self.player_id) or self.check_win(3 - self.player_id) or all(self.board[0] != 0)

    def evaluate(self, player_id): 
        """
        Evaluates the board from the perspective of a specific player.
        
        Args:
           player_id (int): The player to evaluate the board for.

        Returns:
           int: +1000 for a win, -1000 for a loss, 0 otherwise.
        """
        if self.check_win(player_id):
            return 1000
        elif self.check_win(3 - player_id):
            return -1000
        else:
            return 0

    def check_win(self, player): 
        """
        This checks if a player has four pieces in a row somewhere.

        Args:
            player (int): The player we are checking for (1 or 2).

        Returns:
            bool: True if the player won, False if not.
        """
        # Check horizontal wins
        for c in range(self.board.shape[1] - 3):
            for r in range(self.board.shape[0]):
                if all(self.board[r][c+i] == player for i in range(4)):
                    return True
                
        # Check vertical wins
        for c in range(self.board.shape[1]):
            for r in range(self.board.shape[0] - 3):
                if all(self.board[r+i][c] == player for i in range(4)):
                    return True
                
         # Check positive diagonal wins (\ direction)
        for c in range(self.board.shape[1] - 3):
            for r in range(self.board.shape[0] - 3):
                if all(self.board[r+i][c+i] == player for i in range(4)):
                    return True
                
        # Check negative diagonal wins (/ direction)       
        for c in range(self.board.shape[1] - 3):
            for r in range(3, self.board.shape[0]):
                if all(self.board[r-i][c+i] == player for i in range(4)):
                    return True
        return False
