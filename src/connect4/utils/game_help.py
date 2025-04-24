import pygame
from constants import WIDTH, HEIGHT, WHITE, BLACK, FONT

def display_message(message):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BLACK)
    label = FONT.render(message, True, WHITE)
    rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(label, rect)
    pygame.display.update()
    pygame.time.delay(2000)
