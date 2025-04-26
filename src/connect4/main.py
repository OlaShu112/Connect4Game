import pygame
import sys
import time
from constants import *
from agents.random_agent import RandomAgent
from agents.smart_agent import SmartAgent
from agents.minimax_agent import MinimaxAgent
from agents.ml_agent import MLAgent
from utils.board_utils import create_board, drop_piece, valid_move, switch_turn, check_win, board_is_full, block_player_move
from graphics import draw_board
from utils.player_data import save_player_score
from utils.game_help import display_message
from utils.music_player import play_music, stop_music, next_track, previous_track
from utils.game_state import GameState


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

FONT = pygame.font.SysFont("Cambria", 32, bold=True)
BIG_FONT = pygame.font.SysFont("Cambria", 48, bold=True)
CLICK_COOLDOWN = 300  
TURN_TIME_LIMIT = 10  

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
        turn_start_time = time.time()  # Start Turn Timer
        running_turn = True

        while running_turn:
            draw_board(board, turn, screen)
            current_time = pygame.time.get_ticks()

            elapsed_time = int(time.time() - turn_start_time)
            remaining_time = max(TURN_TIME_LIMIT - elapsed_time, 0)

            pygame.display.set_caption(f"Connect 4 - Time Left: {remaining_time}s")  # Update title with countdown

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
                running = False
                break

            col = None

            if mode == "Human-Human":
                if pygame.mouse.get_pressed()[0] and current_time - last_click_time > CLICK_COOLDOWN:
                    col = pygame.mouse.get_pos()[0] // SQUARE_SIZE
                    last_click_time = current_time
            elif mode.startswith("AI") and "AI" in mode:
                pygame.time.delay(800)
                agent = agent1 if turn == 1 else agent2

                if isinstance(agent, MinimaxAgent):
                    game_state = GameState(board.copy(), turn)           
                    col = agent.get_move(game_state)
                else:
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
                    if isinstance(ai_agent, MinimaxAgent):
                        
                        game_state = GameState(board.copy(), turn)
                        col = ai_agent.get_move(game_state)
                    else:
                         col = ai_agent.get_move(board)


            if col is not None and valid_move(board, col):
                row = drop_piece(board, col, turn)
                if row != -1:
                    draw_board(board, turn, screen)
                    if check_win(board, turn):
                        winner = player1_name if turn == 1 else player2_name
                        display_message(f"{winner} wins!")
                        save_player_score(winner, 1)
                        pygame.time.delay(2500)
                        running = False
                        break
                    elif board_is_full(board):
                        display_message("It's a draw!")
                        pygame.time.delay(2500)
                        running = False
                        break

                turn = switch_turn(turn)
                running_turn = False  # End turn after valid move

            if remaining_time <= 0:
                print("⏰ Turn timed out! Switching turn...")
                turn = switch_turn(turn)
                running_turn = False

            pygame.display.update()
            pygame.time.delay(100)  # Smooth update

    if ask_play_again():
        main_menu(player_name)

    else:
        main_menu(player_name)


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

    main_menu(player_name)  # After registration, move to main menu

def main_menu(player_name=None):
    screen.fill(BLACK)
    menu_buttons = show_menu()
    selected_mode = get_mode_selection(menu_buttons)
    play_game(selected_mode, player_name if "AI" not in selected_mode else None)


# ======= MAIN ENTRY POINT =======
if __name__ == "__main__":
    from utils.dataset_loader import DatasetLoader

    loader = DatasetLoader(data_path="connect4_dataset")
    csv_data = loader.load_csv('connect-4.data.csv')
    attributes = loader.load_names('connect-4.names.txt')

    if not csv_data or not attributes:
        print("❌ Error loading dataset. ML Agent may not work properly.")

    AGENTS = {
        "Random": RandomAgent(player_id=2),
        "Smart": SmartAgent(player_id=2),
        "Minimax": MinimaxAgent(player_id=2),
        "ML": MLAgent(player_id=2, data_path="connect4_dataset/connect-4.data.csv", names_path="connect4_dataset/connect-4.names.txt")
    }

    MODES = [
        ("Human vs Human", "Human-Human"),
        ("Human vs Random Agent", "Random"),
        ("Human vs Smart Agent", "Smart"),
        ("Human vs Minimax Agent", "Minimax"),
        ("Human vs ML Agent", "ML"),
        ("AI vs AI (Random vs Smart)", "AI-Random-Smart"),
        ("AI vs AI (Minimax vs Smart)", "AI-Minimax-Smart"),
        ("AI vs AI (Minimax vs ML)", "AI-Minimax-ML")
    ]

    main()



# This is a Connect Four game implementation with options for human, AI vs AI, and player vs AI modes.

## References
# [1] https://www.pygame.org/docs/
# https://scikit-learn.org/stable/
# https://www.youtube.com/watch?v=UYgyRArKDEs&list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV
# https://www.askpython.com/python/examples/connect-four-game
# https://www.youtube.com/watch?v=yzj5TAfPI5Y
# https://labex.io/tutorials/python-connect-four-game-human-vs-ai-298858
# https://www.youtube.com/watch?v=cONc0NcKE7s
# https://www.youtube.com/watch?app=desktop&v=zD-Xuu_Jpe4&t=325s
# https://github.com/Buzzpy/Python-Projects/blob/main/Music_player.py
# https://github.com/hardbyte/python-can/blob/main/can/message.py
# https://github.com/cansozbir/Connect-4
# https://www.geeksforgeeks.org/python-oops-concepts/
# https://www.google.com/search?q=oop+programming+python&sca_esv=912e3b7be34fd981&sxsrf=AHTn8zrCMezWnARfvj5NAbMrvXU05fQsGA%3A1745698157453&source=hp&ei=bT0NaP_AGbq-hbIP5I2Z-Q8&iflsig=ACkRmUkAAAAAaA1LfdW9dLpv9wDOqbAclcQeP9-I4qO7&oq=oop+programming+&gs_lp=Egdnd3Mtd2l6IhBvb3AgcHJvZ3JhbW1pbmcgKgIIATIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIqUtQAFidMnAAeACQAQCYAZoBoAG1CaoBBDE1LjG4AQHIAQD4AQGYAhCgAv0JwgIIEAAYgAQYsQPCAg4QABiABBixAxiDARiKBcICBBAAGAPCAg4QLhiABBixAxjRAxjHAcICERAuGIAEGLEDGNEDGIMBGMcBwgILEAAYgAQYsQMYgwHCAggQLhiABBixA8ICCBAuGIAEGNQCwgINEC4YgAQY0QMYxwEYCsICBxAAGIAEGAqYAwCSBwQxNC4yoAf7X7IHBDE0LjK4B_0J&sclient=gws-wiz#fpstate=ive&vld=cid:563ce64d,vid:Ej_02ICOIgs,st:0
