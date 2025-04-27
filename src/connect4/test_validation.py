from agents.random_agent import RandomAgent
from agents.smart_agent import SmartAgent
from agents.minimax_agent import MinimaxAgent
from agents.ml_agent import MLAgent
from utils.board_utils import create_board, drop_piece, valid_move, board_is_full, check_win, switch_turn
from utils.game_state import GameState
import time

def run_ai_vs_ai_test(agent1, agent2, num_games=500):
    agent1_wins = 0
    agent2_wins = 0
    draws = 0

    for game in range(num_games):
        board = create_board()
        turn = 1  # Player 1 starts

        running = True
        while running:
            agent = agent1 if turn == 1 else agent2

            # Object passed to each agent
            if isinstance(agent, MinimaxAgent):
                move = agent.get_move(GameState(board.copy(), turn))
            elif isinstance(agent, MLAgent):
                move = agent.get_move(board)
            else:
                move = agent.get_move(board)

            if move is not None and valid_move(board, move):
                row = drop_piece(board, move, turn)
                if row != -1:
                    if check_win(board, turn):
                        if turn == 1:
                            agent1_wins += 1
                        else:
                            agent2_wins += 1
                        running = False
                    elif board_is_full(board):
                        draws += 1
                        running = False
                    else:
                        turn = switch_turn(turn)
                else:
                    running = False
            else:
                running = False

        # Optional:  To Show simple progress using bar length
        if (game + 1) % 5 == 0 or (game + 1) == num_games:
            progress = (game + 1) / num_games
            bar_length = 30
            filled_length = int(bar_length * progress)
            bar = "=" * filled_length + "-" * (bar_length - filled_length)
            print(f"\rProgress: [{bar}] {progress*100:.1f}%", end="")


    total = agent1_wins + agent2_wins + draws
    print("\n=== Test Results ===")
    print(f"Total Games: {total}")
    print(f"Agent1 Wins ({agent1.name}): {agent1_wins}")
    print(f"Agent2 Wins ({agent2.name}): {agent2_wins}")
    print(f"Draws: {draws}")
    print(f"Agent1 Win Rate: {agent1_wins/total*100:.2f}%")
    print(f"Agent2 Win Rate: {agent2_wins/total*100:.2f}%")
    print(f"Draw Rate: {draws/total*100:.2f}%")

if __name__ == "__main__":
    # Agents for different tests
    random_agent = RandomAgent(player_id=1)
    smart_agent = SmartAgent(player_id=2)

    smart_agent2 = SmartAgent(player_id=1)
    minimax_agent = MinimaxAgent(player_id=2)

    minimax_agent2 = MinimaxAgent(player_id=1)
    ml_agent = MLAgent(player_id=2, data_path="connect4_dataset/connect-4.data.csv", names_path="connect4_dataset/connect-4.names.txt")

    # Test 1: Random vs Smart
    print("Testing Random vs Smart...")
    run_ai_vs_ai_test(random_agent, smart_agent, num_games=500)

    # Test 2: Smart vs Minimax
    print("\nTesting Smart vs Minimax...")
    run_ai_vs_ai_test(smart_agent2, minimax_agent, num_games=500)

    # Test 3: Minimax vs ML
    print("\nTesting Minimax vs ML...")
    run_ai_vs_ai_test(minimax_agent2, ml_agent, num_games=500)
