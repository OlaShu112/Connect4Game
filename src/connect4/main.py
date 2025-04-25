import pygame
import sys
import time
from constants import *
from agents.random_agent import RandomAgent
from agents.smart_agent import SmartAgent
from agents.minimax_agent import MinimaxAgent
from agents.ml_agent import MLAgent
from utils.board_utils import create_board, drop_piece, valid_move, switch_turn, check_win, board_is_full
from graphics import draw_board
from utils.player_data import save_player_score
from utils.game_help import display_message
from utils.music_player import play_music, stop_music, next_track, previous_track
from utils.board_utils import block_player_move

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

FONT = pygame.font.SysFont("arial", 32)
BIG_FONT = pygame.font.SysFont("arial", 48)
CLICK_COOLDOWN = 300  # milliseconds

TURN_TIME_LIMIT = 10  # seconds

def render_text(text, x, y, color=WHITE, center=True):
    label = FONT.render(text, True, color)
    rect = label.get_rect(center=(x, y)) if center else label.get_rect(topleft=(x, y))
    screen.blit(label, rect)
    return rect

def register_player():
    screen.fill(BLACK)
    name = ""
    render_text("Register Player - Enter Your Name:", WIDTH // 2, HEIGHT // 2 - 40)
    pygame.display.flip()

    while True:
        screen.fill(BLACK)
        render_text("Register Player - Enter Your Name:", WIDTH // 2, HEIGHT // 2 - 40)
        render_text(name + "_", WIDTH // 2, HEIGHT // 2 + 10)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isprintable():
                    name += event.unicode

def show_menu():
    screen.fill(BLACK)
    render_text("Select Game Mode", WIDTH // 2, 50, YELLOW)
    buttons = []
    for i, (label, mode) in enumerate(MODES):
        rect = render_text(label, WIDTH // 2, 120 + i * 50)
        buttons.append((rect, mode))
    pygame.display.flip()
    return buttons

def get_mode_selection(buttons):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, mode in buttons:
                    if rect.collidepoint(event.pos):
                        return mode

def ask_play_again():
    screen.fill(BLACK)
    render_text("Play Again? Y/N", WIDTH // 2, HEIGHT // 2, YELLOW)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

def play_game(mode, player_name=None):
    board = create_board()
    turn = 1
    draw_board(board, turn, screen)
    last_click_time = 0

    if mode == "Human-Human":
        player1_name = "Player 1"
        player2_name = "Player 2"
        ai_agent = None
    elif "AI" in mode and mode.startswith("AI"):
        agent1 = AGENTS["Random"] if "Random" in mode else AGENTS["Minimax"]
        agent2 = AGENTS["Smart"] if "Smart" in mode else AGENTS["ML"]
        player1_name = "Agent 1"
        player2_name = "Agent 2"
    else:
        ai_agent = AGENTS[mode]
        player1_name = player_name or "Player 1"
        player2_name = "AI"

    running = True
    while running:
        draw_board(board, turn, screen)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    play_music()
                elif event.key == pygame.K_s:
                    stop_music()
                elif event.key == pygame.K_RIGHT:
                    next_track()
                elif event.key == pygame.K_LEFT:
                    previous_track()

        if board_is_full(board):
            display_message("It's a draw!")
            save_player_score(player1_name, 0.5)
            save_player_score(player2_name, 0.5)
            pygame.time.delay(2500)
            break

        col = None

        if mode == "Human-Human":
            if pygame.mouse.get_pressed()[0] and current_time - last_click_time > CLICK_COOLDOWN:
                col = pygame.mouse.get_pos()[0] // SQUARE_SIZE
                last_click_time = current_time
        elif mode.startswith("AI") and "AI" in mode:
            pygame.time.delay(800)
            agent = agent1 if turn == 1 else agent2
            col = agent.get_move(board)
        elif turn == 1:
            if pygame.mouse.get_pressed()[0] and current_time - last_click_time > CLICK_COOLDOWN:
                col = pygame.mouse.get_pos()[0] // SQUARE_SIZE
                last_click_time = current_time
        else:
            pygame.time.delay(800)
            opponent = 1 if turn == 2 else 2
            block_col = block_player_move(board, opponent)
            if block_col != -1 and valid_move(board, block_col):
                col = block_col
            else:
                col = ai_agent.get_move(board)

        if col is None or not valid_move(board, col):
            continue

        row = drop_piece(board, col, turn)
        if row != -1:
            draw_board(board, turn, screen)
            if check_win(board, turn):
                winner = player1_name if turn == 1 else player2_name
                display_message(f"{winner} wins!")
                save_player_score(winner, 1)
                pygame.time.delay(2500)
                break
            elif board_is_full(board):
                display_message("It's a draw!")
                pygame.time.delay(2500)
                break

        turn = switch_turn(turn)

    if ask_play_again():
        main()
    else:
        pygame.quit()
        sys.exit()

def main():
    ask_register = True
    player_name = None

    screen.fill(BLACK)
    render_text("Do you want to register? (Y/N)", WIDTH // 2, HEIGHT // 2 - 20)
    pygame.display.flip()

    while ask_register:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    player_name = register_player()
                    ask_register = False
                elif event.key == pygame.K_n:
                    ask_register = False

    menu_buttons = show_menu()
    selected_mode = get_mode_selection(menu_buttons)
    play_game(selected_mode, player_name if "AI" not in selected_mode else None)

# ========== EXECUTION ENTRY POINT ==========
if __name__ == "__main__":
    AGENTS = {
        "Random": RandomAgent(player_id=2),
        "Smart": SmartAgent(player_id=2),
        "Minimax": MinimaxAgent(player_id=2),
        "ML": MLAgent(player_id=2)
    }

    MODES = [
        ("Human vs Human", "Human-Human"),
        ("Human vs Random Agent", "Random"),
        ("Human vs Smart Agent", "Smart"),
        ("Human vs Minimax Agent", "Minimax"),
        ("Human vs ML Agent", "ML"),
        ("AI vs AI (Random vs Smart)", "AI-Random-Smart"),
        ("AI vs AI (Minimax vs ML)", "AI-Minimax-ML")
    ]

    main()
