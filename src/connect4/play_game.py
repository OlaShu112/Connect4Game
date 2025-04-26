import pygame
import sys
import time
import random
from constants import *
from utils.board_utils import create_board, drop_piece, valid_move, switch_turn, check_win, board_is_full
from graphics import draw_board
from agents.random_agent import RandomAgent
from agents.smart_agent import SmartAgent
from agents.minimax_agent import MinimaxAgent
from agents.ml_agent import MLAgent
from utils.player_data import save_player_score
from utils.game_help import display_message

# Reusable agents dictionary
AGENTS = {
    "Random": RandomAgent(player_id=2),
    "Smart": SmartAgent(player_id=2),
    "Minimax": MinimaxAgent(player_id=2),
    "ML": MLAgent(player_id=2)
}

TURN_TIME_LIMIT = 10  

def play_game(mode, player_name=None, screen=None):
    board = create_board()
    turn = 1
    draw_board(board, turn, screen)

    if "AI" in mode and mode.startswith("AI"):
        agent1 = AGENTS["Random"] if "Random" in mode else AGENTS["Minimax"]
        agent2 = AGENTS["Smart"] if "Smart" in mode else AGENTS["ML"]
        player1_name = "Agent 1"
        player2_name = "Agent 2"
        ai_mode = True
    else:
        ai_agent = AGENTS[mode]
        player1_name = player_name or "Player 1"
        player2_name = "AI"
        ai_mode = False

    running = True
    last_mouse_pressed = False

    while running:
        if board_is_full(board):
            draw_board(board, turn, screen)
            display_message("It's a draw!")
            save_player_score(player1_name, 0.5)
            save_player_score(player2_name, 0.5)
            pygame.time.delay(2500)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not ai_mode and (turn == 1 or mode == "Human-Human"):
            turn_start_time = time.time()  # Human's turn with timer
            move_made = False

            while not move_made:
                elapsed_time = int(time.time() - turn_start_time)
                remaining_time = max(TURN_TIME_LIMIT - elapsed_time, 0)

                pygame.display.set_caption(f"Connect 4 - Time Left: {remaining_time}s")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        col = pygame.mouse.get_pos()[0] // SQUARE_SIZE
                        if valid_move(board, col):
                            drop_piece(board, col, turn)
                            move_made = True
                            break

                if remaining_time <= 0:
                    print("⏰ Turn timed out! Skipping move...")
                    turn = switch_turn(turn)
                    move_made = True
                    break

                pygame.display.update()
                pygame.time.delay(100)

        else:
            pygame.time.delay(800)  # AI move
            if mode.startswith("AI") and "AI" in mode:
                agent = agent1 if turn == 1 else agent2
                move = agent.get_move(board)
            else:
                move = ai_agent.get_move(board)

            if valid_move(board, move):
                drop_piece(board, move, turn)

        draw_board(board, turn, screen)

        if check_win(board, turn):
            draw_board(board, turn, screen)
            winner = player1_name if turn == 1 else player2_name
            display_message(f"{winner} wins!")
            save_player_score(winner, 1)
            pygame.time.delay(2500)
            break

        if not (not ai_mode and (turn == 1 or mode == "Human-Human") and remaining_time <= 0): # Only switch if it wasn't skipped due to timeout
            turn = switch_turn(turn)
