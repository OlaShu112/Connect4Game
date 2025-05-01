import random
import numpy as np
import time
import sys
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from connect4.agents.minimax_agent import MinimaxAgent
from connect4.agents.random_agent import RandomAgent
from connect4.game import Connect4Game


class Evaluation:
    def __init__(self, game, num_games=100):
        self.game = game
        self.num_games = num_games
        self.results = defaultdict(int)  # Store results (win, loss, draw) counts

    def play_game(self, player1, player2):
        self.game.reset()
        current_player = 1  # Player 1 starts
        last_row = -1 
        last_col = -1
        
        while not self.game.is_game_over():
            if current_player == 1:
                move = player1.get_move(self.game.get_board_copy())
            else:
                move = player2.get_move(self.game.get_board_copy()) 
                
            row = self.game.make_move(move)
            last_row = row  # store last move
            last_col = move
            current_player = 3 - current_player  # Switch between Player 1 and Player 2
        
        # Determine the winner or draw
        if self.game.check_winner(last_row, last_col):
            winner_player = 3 - current_player
            return 'player1' if winner_player == 1 else 'player2'
        else:
            return 'draw'

 
    def evaluate_agents(self, agent1, agent2):
        start_time = time.time()  # Start timing

        bar_length = 30  # Length of the progress bar

        for game_num in range(self.num_games):
            result = self.play_game(agent1, agent2)
            self.results[result] += 1

            # Progress bar calculation
            progress = (game_num + 1) / self.num_games
            filled_length = int(bar_length * progress)
            bar = "#" * filled_length + "-" * (bar_length - filled_length)
            percent = progress * 100

            # Progress bar
            sys.stdout.write(f"\rEvaluating: [{bar}] {percent:.1f}%")
            sys.stdout.flush()

        end_time = time.time()
        total_time = end_time - start_time

        print(f"\n✅ Evaluation Complete in {total_time:.2f} seconds!\n")
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


    def save_results_graph(self, agent1_name, agent2_name, save_path='reports/evaluation_result.png'):
        labels = ['Agent 1 Wins', 'Agent 2 Wins', 'Draws']
        values = [self.results['player1'], self.results['player2'], self.results['draw']]

        plt.figure(figsize=(6, 4))
        bars = plt.bar(labels, values)
        plt.title(f"{agent1_name} vs {agent2_name} Evaluation Results")
        plt.ylabel("Games Won")

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.5, f'{int(yval)}',
                 ha='center', va='bottom')

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        print(f"📊 Graph saved to {save_path}")


if __name__ == "__main__":
    from connect4.agents.random_agent import RandomAgent
    from connect4.game import Connect4Game  

    game = Connect4Game() 
    evaluation = Evaluation(game)
    agent1 = RandomAgent(player_id=1)
    agent2 = RandomAgent(player_id=2)

    evaluation.evaluate_agents(agent1, agent2)
    evaluation.print_evaluation_results()

    evaluation.save_results_graph(agent1.__class__.__name__, agent2.__class__.__name__)

