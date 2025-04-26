import pygame

# Constants for the Connect 4 game
SQUARE_SIZE = 100
ROW_COUNT = 6
COLUMN_COUNT = 7
WIDTH = SQUARE_SIZE * COLUMN_COUNT
HEIGHT = SQUARE_SIZE * (ROW_COUNT + 1)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (70, 130, 200)


# Initialize fonts
pygame.font.init()
FONT = pygame.font.SysFont("arial", 32)
BIG_FONT = pygame.font.SysFont("arial", 48)

TURN_TIME_LIMIT = 10  # seconds