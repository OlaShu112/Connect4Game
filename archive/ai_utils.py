from ..src.connect4.utils.board_utils import valid_move, drop_piece, check_win, board_is_full, switch_turn
from ..src.connect4.utils.game_help import display_message
from graphics import draw_board
from utils.game_state import GameState  # Ensure this exists and has the required methods

def block_player_move(board, player):
    for col in range(len(board[0])):
        if valid_move(board, col):
            temp_board = [row.copy() for row in board]
            row = drop_piece(temp_board, col, player)
            if check_win(temp_board, player):
                return col
    return -1

def ai_move(board, agent, turn, label, screen):
    opponent = 1 if turn == 2 else 2
    block_col = block_player_move(board, opponent)

    try:
        # Block opponent if they have a winning move
        if block_col != -1 and valid_move(board, block_col):
            col = block_col
        else:
            # Use GameState if agent expects it (e.g., Minimax)
            if hasattr(agent, "get_move"):
                if "Minimax" in str(agent):
                    col = agent.get_move(GameState(board.copy(), turn))
                else:
                    col = agent.get_move(board)
            else:
                col = agent(board, turn)

        if not isinstance(col, int):
            raise ValueError(f"{label} provided an invalid column: {col}")

        if not valid_move(board, col):
            print(f"{label} chose invalid column {col}.")
            return False

        row = drop_piece(board, col, turn)
        if row != -1:
            draw_board(board, turn, screen)

            if check_win(board, turn):
                display_message(f"{label} wins!")
                return True
            elif board_is_full(board):
                display_message("It's a draw!")
                return True

            draw_board(board, switch_turn(turn), screen)

        return False

    except Exception as e:
        print(f"AI move generation failed for {label}: {e}")
        return False
