import random
import numpy as np
from collections import defaultdict
from connect4.agents.minimax_agent import MinimaxAgent
from connect4.agents.random_agent import RandomAgent

class Evaluation:
    def __init__(self, game, num_games=100):
        """
        Initializes the evaluation class with the game instance and number of games to simulate.
        
        :param game: The game instance to evaluate.
        :param num_games: Number of games to simulate for evaluation.
        """
        self.game = game
        self.num_games = num_games
        self.results = defaultdict(int)  # Store results (win, loss, draw) counts

    def play_game(self, player1, player2):
        """
        Plays a single game between two AI players (or human vs AI).
        
        :param player1: The first player (either human or AI).
        :param player2: The second player (either human or AI).
        :return: The result of the game ('player1', 'player2', or 'draw').
        """
        self.game.reset_board()
        current_player = 1  # Player 1 starts
        
        while not self.game.is_game_over():
            if current_player == 1:
                move = player1.get_move(self.game)
            else:
                move = player2.get_move(self.game)
                
            self.game.make_move(move, current_player)
            current_player = 3 - current_player  # Switch between Player 1 and Player 2
        
        # Determine the winner or draw
        if self.game.check_winner(1):
            return 'player1'
        elif self.game.check_winner(2):
            return 'player2'
        else:
            return 'draw'

    def evaluate_agents(self, agent1, agent2):
        """
        Evaluates two agents by running multiple games against each other.

        :param agent1: The first agent to evaluate.
        :param agent2: The second agent to evaluate.
        :return: A dictionary with the results of the games.
        """
        for game_num in range(self.num_games):
            print(f"Evaluating game {game_num + 1} of {self.num_games}...")
            result = self.play_game(agent1, agent2)
            self.results[result] += 1

        return self.results

    def print_evaluation_results(self):
        """
        Prints the evaluation results (wins, losses, draws) for the agents.
        """
        print("\nEvaluation Complete!")
        print(f"Total Games Played: {self.num_games}")
        print(f"Agent 1 Wins: {self.results['player1']}")
        print(f"Agent 2 Wins: {self.results['player2']}")
        print(f"Draws: {self.results['draw']}")

    def evaluate_vs_random(self, agent, num_games=100):
        """
        Evaluates a given agent against a random agent.
        
        :param agent: The agent to evaluate.
        :param num_games: Number of games to simulate against the random agent.
        """
        random_agent = RandomAgent(self.game)
        print(f"Evaluating {agent.__class__.__name__} vs Random Agent...")
        self.num_games = num_games
        self.results.clear()  # Clear previous results
        self.evaluate_agents(agent, random_agent)
        self.print_evaluation_results()

    def evaluate_vs_minimax(self, agent, num_games=100):
        """
        Evaluates a given agent against a minimax agent.
        
        :param agent: The agent to evaluate.
        :param num_games: Number of games to simulate against the minimax agent.
        """
        minimax_agent = MinimaxAgent(self.game)
        print(f"Evaluating {agent.__class__.__name__} vs Minimax Agent...")
        self.num_games = num_games
        self.results.clear()  # Clear previous results
        self.evaluate_agents(agent, minimax_agent)
        self.print_evaluation_results()

    def evaluate_ai_vs_ai(self, agent1, agent2, num_games=100):
        """
        Evaluates two agents by playing against each other.
        
        :param agent1: The first agent.
        :param agent2: The second agent.
        :param num_games: Number of games to simulate between the two agents.
        """
        print(f"Evaluating {agent1.__class__.__name__} vs {agent2.__class__.__name__}...")
        self.num_games = num_games
        self.results.clear()  # Clear previous results
        self.evaluate_agents(agent1, agent2)
        self.print_evaluation_results()

