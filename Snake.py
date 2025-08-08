import pygame
import random
import string

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alphabet Snake Game")

# Fonts
font = pygame.font.SysFont("Arial", 20)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# Directions
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

# Initial snake
snake = [(5, 5)]  # one segment
collected_letters = []  # grows as we collect food
direction = "RIGHT"

# Generate new food
def get_new_letter():
    while True:
        pos = (random.randint(0, (WIDTH // CELL_SIZE) - 1),
               random.randint(0, (HEIGHT // CELL_SIZE) - 1))
        if pos not in snake:
            break
    letter = random.choice(string.ascii_uppercase)
    return pos, letter

food_pos, food_letter = get_new_letter()

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != "DOWN":
        direction = "UP"
    elif keys[pygame.K_DOWN] and direction != "UP":
        direction = "DOWN"
    elif keys[pygame.K_LEFT] and direction != "RIGHT":
        direction = "LEFT"
    elif keys[pygame.K_RIGHT] and direction != "LEFT":
        direction = "RIGHT"

    # Move snake
    dx, dy = DIRECTIONS[direction]
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)

    # Check collision
    if (new_head[0] < 0 or new_head[0] >= WIDTH // CELL_SIZE or
        new_head[1] < 0 or new_head[1] >= HEIGHT // CELL_SIZE or
        new_head in snake):
        print("Game Over!")
        running = False
        continue

    snake.insert(0, new_head)

    # Eat food
    if new_head == food_pos:
        collected_letters.append(food_letter)
        food_pos, food_letter = get_new_letter()
    else:
        snake.pop()  # tail movement

    # Draw food
    food_text = font.render(food_letter, True, RED)
    screen.blit(food_text, (food_pos[0]*CELL_SIZE, food_pos[1]*CELL_SIZE))

    # Draw snake
    for i, segment in enumerate(snake):
        if i == 0 and len(collected_letters) == 0:
            # First step: head only
            letter = "?"
        elif i < len(snake) - len(collected_letters):
            letter = "?"
        else:
            # Show collected letters at tail in order
            letter_index = i - (len(snake) - len(collected_letters))
            letter = collected_letters[letter_index]
        text = font.render(letter, True, GREEN)
        screen.blit(text, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE))

    pygame.display.update()
    clock.tick(10)

pygame.quit()
