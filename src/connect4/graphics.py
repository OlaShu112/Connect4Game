import pygame
from connect4.constants import SQUARE_SIZE, ROW_COUNT, COLUMN_COUNT, BLUE, BLACK, RED, YELLOW

def draw_board(board, turn, screen):
    screen.fill(BLACK)

    # Always show the hover circle, but color depends on turn
    hover_color = RED if turn == 1 else YELLOW
    mouse_x = pygame.mouse.get_pos()[0]
    hover_x = mouse_x // SQUARE_SIZE * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.circle(screen, hover_color, (hover_x, SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

    # Draw the board grid and pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            color = BLACK
            if board[r][c] == 1:
                color = RED
            elif board[r][c] == 2:
                color = YELLOW
            pygame.draw.circle(screen, color, (
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                int((r + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)
            ), SQUARE_SIZE // 2 - 5)

    pygame.display.update()
