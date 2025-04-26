import random
import numpy as np
from collections import defaultdict
from connect4.agents.minimax_agent import MinimaxAgent
from connect4.agents.random_agent import RandomAgent

class Evaluation:
    def __init__(self, game, num_games=100):
        self.game = game
        self.num_games = num_games
        self.results = defaultdict(int)  # Store results (win, loss, draw) counts

    def play_game(self, player1, player2):
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
        random_agent = RandomAgent(self.game)
        print(f"Evaluating {agent.__class__.__name__} vs Random Agent...")
        self.num_games = num_games
        self.results.clear()  # Clear previous results
        self.evaluate_agents(agent, random_agent)
        self.print_evaluation_results()

    def evaluate_vs_minimax(self, agent, num_games=100):
        minimax_agent = MinimaxAgent(self.game)
        print(f"Evaluating {agent.__class__.__name__} vs Minimax Agent...")
        self.num_games = num_games
        self.results.clear()  # Clear previous results
        self.evaluate_agents(agent, minimax_agent)
        self.print_evaluation_results()

    def evaluate_ai_vs_ai(self, agent1, agent2, num_games=100):
        print(f"Evaluating {agent1.__class__.__name__} vs {agent2.__class__.__name__}...")
        self.num_games = num_games
        self.results.clear()  # Clear previous results
        self.evaluate_agents(agent1, agent2)
        self.print_evaluation_results()

