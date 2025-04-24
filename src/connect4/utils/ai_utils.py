from .board_utils import valid_move, drop_piece, check_win, board_is_full, switch_turn
from graphics import draw_board



def block_player_move(board, player):
    from .board_utils import valid_move, drop_piece, check_win
    for col in range(len(board[0])):
        if valid_move(board, col):
            temp_board = [row.copy() for row in board]
            row = drop_piece(temp_board, col, player)
            if check_win(temp_board, player):
                return col
    return -1

def ai_move(board, agent, turn, label, screen):
    from .board_utils import valid_move, drop_piece, check_win, board_is_full, switch_turn, draw_board
    from .game_help import display_message
    from .ai_utils import block_player_move

    opponent = 1 if turn == 2 else 2
    block_col = block_player_move(board, opponent)

    if block_col != -1 and valid_move(board, block_col):
        col = block_col
    else:
        try:
            col = agent.get_move(board) if hasattr(agent, "get_move") else agent(board, turn)
        except Exception as e:
            print(f"AI move generation failed for {label}: {e}")
            return False

    try:
        col = int(float(col))
    except (ValueError, TypeError):
        print(f"Invalid column received from {label}: {col}")
        return False

    valid_cols = [c for c in range(len(board[0])) if board[0][c] == 0]
    if col not in valid_cols:
        print(f"{label} couldn't find a valid move. Skipping turn.")
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
