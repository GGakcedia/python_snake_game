import pygame
import time
import random
 
# Initialize pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
DARKER_GREEN = (0, 50, 0)
BLUE = (0, 0, 255)
LIGHT_GREEN = (144, 238, 144)

# Set up the clock
clock = pygame.time.Clock()
SNAKE_BLOCK = 20
SNAKE_SPEED = 10

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 25)

def your_score(score):
    banner_height = 50
    pygame.draw.rect(screen, DARKER_GREEN, [0, 0, WIDTH, banner_height])
    pygame.draw.circle(screen, RED, (WIDTH // 2 - 30, banner_height // 2), 10)
    value = score_font.render(str(score), True, WHITE)
    screen.blit(value, [WIDTH // 2, banner_height // 2 - value.get_height() // 2])

def our_snake(block, snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, BLUE, [segment[0], segment[1], block, block])

def draw_walls():
    wall_thickness = SNAKE_BLOCK
    pygame.draw.rect(screen, DARK_GREEN, [0, 50, wall_thickness, HEIGHT - 50])  # Left wall
    pygame.draw.rect(screen, DARK_GREEN, [0, HEIGHT - wall_thickness, WIDTH, wall_thickness])  # Bottom wall
    pygame.draw.rect(screen, DARK_GREEN, [WIDTH - wall_thickness, 50, wall_thickness, HEIGHT - 50])  # Right wall
    pygame.draw.rect(screen, DARK_GREEN, [0, 50, WIDTH, wall_thickness])  # Top wall

def game_over_screen():
    while True:
        screen.fill(GREEN)
        pygame.draw.rect(screen, DARKER_GREEN, [0, 0, WIDTH, SNAKE_BLOCK * 3])  # Top banner
        pygame.draw.rect(screen, DARKER_GREEN, [0, HEIGHT - SNAKE_BLOCK * 3, WIDTH, SNAKE_BLOCK * 3])  # Bottom banner

        message_font = pygame.font.SysFont("comicsansms", 50)
        message = message_font.render("Game Over", True, WHITE)
        screen.blit(message, [WIDTH / 2 - message.get_width() / 2, HEIGHT / 3])

        button_font = pygame.font.SysFont("bahnschrift", 35)
        retry_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2, 200, 50)
        exit_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 70, 200, 50)

        pygame.draw.rect(screen, DARKER_GREEN, retry_button)
        pygame.draw.rect(screen, DARKER_GREEN, exit_button)

        retry_text = button_font.render("Retry", True, WHITE)
        exit_text = button_font.render("Exit", True, WHITE)

        screen.blit(retry_text, [retry_button.x + (retry_button.width - retry_text.get_width()) / 2, retry_button.y + 10])
        screen.blit(exit_text, [exit_button.x + (exit_button.width - exit_text.get_width()) / 2, exit_button.y + 10])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    game_loop()
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()

def game_loop():
    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(SNAKE_BLOCK, WIDTH - 2 * SNAKE_BLOCK) / 20.0) * 20.0
    foody = round(random.randrange(50 + SNAKE_BLOCK, HEIGHT - 2 * SNAKE_BLOCK) / 20.0) * 20.0

    while not game_over:
        while game_close:
            game_over_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        x1 += x1_change
        y1 += y1_change
        
        # Check collision with walls
        if (x1 < SNAKE_BLOCK or x1 >= WIDTH - SNAKE_BLOCK or 
            y1 < 50 + SNAKE_BLOCK or y1 >= HEIGHT - SNAKE_BLOCK):
            game_close = True

        screen.fill(LIGHT_GREEN)
        draw_walls()
        pygame.draw.rect(screen, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        your_score(length_of_snake - 1)
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(SNAKE_BLOCK, snake_list)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(SNAKE_BLOCK, WIDTH - 2 * SNAKE_BLOCK) / 20.0) * 20.0
            foody = round(random.randrange(50 + SNAKE_BLOCK, HEIGHT - 2 * SNAKE_BLOCK) / 20.0) * 20.0
            length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

game_loop()