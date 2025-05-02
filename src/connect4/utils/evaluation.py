import tracemalloc
import random
import numpy as np
import time
import sys
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
from connect4.agents.minimax_agent import MinimaxAgent
from connect4.agents.random_agent import RandomAgent
from connect4.agents.smart_agent import SmartAgent
from connect4.agents.ml_agent import MLAgent
from connect4.game import Connect4Game
from connect4.utils.game_state import GameState


class Evaluation:
    def __init__(self, game, num_games=100):
        self.game = game
        self.num_games = num_games

        self.results = defaultdict(int)
        self.move_counts = []
        self.memory_usages = []

    def play_game(self, player1, player2):
        self.game.reset()
        current_player = 1
        last_row = -1
        last_col = -1
        move_count = 0

        while not self.game.is_game_over():
            board_copy = self.game.get_board_copy()
            valid_moves = self.game.get_valid_moves()

            if not valid_moves:
                break  # No valid moves left, considered draw

            if current_player == 1:
                if isinstance(player1, MinimaxAgent):
                    move = player1.get_move(GameState(board_copy, current_player))
                else:
                    move = player1.get_move(board_copy)
            else:
                if isinstance(player2, MinimaxAgent):
                    move = player2.get_move(GameState(board_copy, current_player))
                else:
                    move = player2.get_move(board_copy)
            
            if move not in valid_moves:
                move = random.choice(valid_moves)

            row = self.game.make_move(move)
            last_row = row
            last_col = move
            current_player = 3 - current_player
            move_count += 1

        self.move_counts.append(move_count)

        if self.game.check_winner(last_row, last_col):
            winner_player = 3 - current_player
            return 'player1' if winner_player == 1 else 'player2'
        else:
            return 'draw'


    def evaluate_agents(self, agent1, agent2):
        start_time = time.time()
        bar_length = 30
        tracemalloc.start()

        for game_num in range(self.num_games):
            result = self.play_game(agent1, agent2)
            self.results[result] += 1

            progress = (game_num + 1) / self.num_games
            filled_length = int(bar_length * progress)
            bar = "=" * filled_length + "-" * (bar_length - filled_length)
            percent = progress * 100
            sys.stdout.write(f"\rEvaluating: [{bar}] {percent:.1f}%")
            sys.stdout.flush()

        current, peak = tracemalloc.get_traced_memory()
        self.memory_usages.append(peak / 1024 / 1024)  # MB
        tracemalloc.stop()

        end_time = time.time()
        print(f"\n✅ Evaluation Complete in {end_time - start_time:.2f} seconds!\n")
        return self.results

    def print_evaluation_results(self):
        print("Evaluation Complete!")
        print(f"Total Games Played: {self.num_games}")
        print(f"Agent 1 Wins: {self.results['player1']}")
        print(f"Agent 2 Wins: {self.results['player2']}")
        print(f"Draws: {self.results['draw']}")

        if self.move_counts:
            avg_moves = sum(self.move_counts) / len(self.move_counts)
            print(f"🕒 Average Game Length (moves): {avg_moves:.2f}")
        if self.memory_usages:
            avg_memory = sum(self.memory_usages) / len(self.memory_usages)
            print(f"🖥️ Peak Memory Usage: {avg_memory:.2f} MB")

    def save_results_graph(self, agent1_name, agent2_name, save_path):
        labels = ['Agent 1 Wins', 'Agent 2 Wins', 'Draws']
        values = [self.results['player1'], self.results['player2'], self.results['draw']]

        plt.figure(figsize=(6, 4))
        bars = plt.bar(labels, values)
        plt.title(f"{agent1_name} vs {agent2_name} Evaluation Results")
        plt.ylabel("Games Won")

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.5, f'{int(yval)}', ha='center', va='bottom')

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        print(f"📊 Graph saved to {save_path}")


if __name__ == "__main__":
    game = Connect4Game()
    evaluation = Evaluation(game, num_games=500) # Tested 50 and 100

    # Random vs Smart
    agent1 = RandomAgent(player_id=1)
    agent2 = SmartAgent(player_id=2)
    print("Testing: RandomAgent vs SmartAgent")
    evaluation.results.clear()
    evaluation.evaluate_agents(agent1, agent2)
    evaluation.print_evaluation_results()
    evaluation.save_results_graph("RandomAgent", "SmartAgent", save_path="reports/Random_vs_Smart.png")

    # Smart vs Minimax
    agent1 = SmartAgent(player_id=1)
    agent2 = MinimaxAgent(player_id=2)
    print("\nTesting: SmartAgent vs MinimaxAgent")
    evaluation.results.clear()
    evaluation.evaluate_agents(agent1, agent2)
    evaluation.print_evaluation_results()
    evaluation.save_results_graph("SmartAgent", "MinimaxAgent", save_path="reports/Smart_vs_Minimax.png")

    # Minimax vs ML
    agent1 = MinimaxAgent(player_id=1)
    agent2 = MLAgent(player_id=2, data_path="connect4_dataset/connect-4.data.csv", names_path="connect4_dataset/connect-4.names.txt")
    print("\nTesting: MinimaxAgent vs MLAgent")
    evaluation.results.clear()
    evaluation.evaluate_agents(agent1, agent2)
    evaluation.print_evaluation_results()
    evaluation.save_results_graph("MinimaxAgent", "MLAgent", save_path="reports/Minimax_vs_ML.png")
