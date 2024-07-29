import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 640
screen_height = 480

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Fonts
font_large = pygame.font.Font(None, 100)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Initialize mixer
pygame.mixer.init()

# Load sound effects
start_sound = pygame.mixer.Sound('/Users/norim/Music/Start_Song.mp3')
eat_sound = pygame.mixer.Sound('/Users/norim/Music/Eating_Effect.mp3')
game_over_sound = pygame.mixer.Sound('/Users/norim/Music/game over sound effect.mp3')

# Function to display text
def display_text(text, font, color, center):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=center)
    screen.blit(text_obj, text_rect)

# Starting screen function
def starting_screen():
    start_sound.play()  # Play start sound
    while True:
        screen.fill(black)
        
        display_text('Snake Game', font_large, green, (screen_width // 2, screen_height // 2 - 100))
        display_text('Press any key to start', font_medium, red, (screen_width // 2, screen_height // 2 + 120))
        display_text('Instructions:', font_small, white, (screen_width // 2, screen_height // 2 - 20))
        display_text('Use arrow keys to move the snake', font_small, white, (screen_width // 2, screen_height // 2 + 10))
        display_text('Eat the red food to grow', font_small, white, (screen_width // 2, screen_height // 2 + 40))
        display_text('Don\'t run into the walls or yourself', font_small, white, (screen_width // 2, screen_height // 2 + 70))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        
        pygame.display.flip()

# Ending screen function
def ending_screen(score):
    game_over_sound.play()  # Play game over sound
    while True:
        screen.fill(black)
        
        display_text('Game Over', font_large, red, (screen_width // 2, screen_height // 2 - 50))
        display_text(f'Your Score: {score}', font_small, white, (screen_width // 2, screen_height // 2))
        display_text('Press any key to play again', font_small, white, (screen_width // 2, screen_height // 2 + 50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        
        pygame.display.flip()

# Main game function
def game():
    clock = pygame.time.Clock()
    
    snake_size = 20
    snake_speed = 10
    snake = [(screen_width // 2, screen_height // 2)]
    snake_direction = pygame.K_RIGHT
    food_pos = (random.randint(0, (screen_width - snake_size) // snake_size) * snake_size,
                random.randint(0, (screen_height - snake_size) // snake_size) * snake_size)
    score = 0
    level = 1
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    snake_direction = event.key
        
        head_x, head_y = snake[0]
        if snake_direction == pygame.K_UP:
            head_y -= snake_size
        elif snake_direction == pygame.K_DOWN:
            head_y += snake_size
        elif snake_direction == pygame.K_LEFT:
            head_x -= snake_size
        elif snake_direction == pygame.K_RIGHT:
            head_x += snake_size
        
        if head_x < 0 or head_x >= screen_width or head_y < 0 or head_y >= screen_height or (head_x, head_y) in snake:
            break
        
        snake.insert(0, (head_x, head_y))
        if (head_x, head_y) == food_pos:
            eat_sound.play()  # Play eat sound
            score += 10
            if score % 50 == 0:
                level += 1
                snake_speed += 5
            food_pos = (random.randint(0, (screen_width - snake_size) // snake_size) * snake_size,
                        random.randint(0, (screen_height - snake_size) // snake_size) * snake_size)
        else:
            snake.pop()
        
        screen.fill(black)
        for segment in snake:
            pygame.draw.rect(screen, green, (*segment, snake_size, snake_size))
        pygame.draw.rect(screen, red, (*food_pos, snake_size, snake_size))
        
        display_text(f'Score: {score}', font_small, white, (screen_width - 100, 20))
        display_text(f'Level: {level}', font_small, white, (screen_width - 100, 50))
        
        pygame.display.flip()
        clock.tick(snake_speed)

    ending_screen(score)

# Main loop
while True:
    starting_screen()
    game()
