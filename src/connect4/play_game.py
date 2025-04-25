import pygame
import sys
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

def play_game(mode, player_name=None, screen=None):
    board = create_board()
    turn = 1
    draw_board(board, turn, screen)

    if "AI" in mode and mode.startswith("AI"):
        agent1 = AGENTS["Random"] if "Random" in mode else AGENTS["Minimax"]
        agent2 = AGENTS["Smart"] if "Smart" in mode else AGENTS["ML"]
        player1_name = "Agent 1"
        player2_name = "Agent 2"
    else:
        ai_agent = AGENTS[mode]
        player2_name = "AI"
        player1_name = player_name or "Player 1"

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

        if mode.startswith("AI") and "AI" in mode:
            pygame.time.delay(800)
            agent = agent1 if turn == 1 else agent2
            move = agent.get_move(board)
            drop_piece(board, move, turn)

        elif turn == 1:
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if mouse_pressed and not last_mouse_pressed:
                col = pygame.mouse.get_pos()[0] // SQUARE_SIZE
                if valid_move(board, col):
                    drop_piece(board, col, turn)
                else:
                    last_mouse_pressed = mouse_pressed
                    continue
            else:
                last_mouse_pressed = mouse_pressed
                draw_board(board, turn, screen)
                continue
            last_mouse_pressed = mouse_pressed

        else:
            pygame.time.delay(800)
            move = ai_agent.get_move(board)
            drop_piece(board, move, turn)

        draw_board(board, turn, screen)

        if check_win(board, turn):
            draw_board(board, turn, screen)
            winner = player1_name if turn == 1 else player2_name
            display_message(f"{winner} wins!")
            save_player_score(winner, 1)
            pygame.time.delay(2500)
            break

        turn = switch_turn(turn)
