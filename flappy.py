import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Game variables
GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_SPEED = 5
PIPE_GAP = 150

# Load and resize bird image
bird_img = pygame.image.load('bird.png')  # Load the bird image
bird_img = pygame.transform.scale(bird_img, (50, 35))  # Resize (width, height)
bird_rect = bird_img.get_rect(center=(100, SCREEN_HEIGHT // 2))  # Get the rect for positioning

# Pipe variables
pipe_width = 70

# Font for score a
font = pygame.font.SysFont('Arial', 30)
# Create a larger font for the "Game Over" message
game_over_font = pygame.font.SysFont('Arial', 50) 
restart_font = pygame.font.SysFont('Arial', 30) 
# Clock for frame rate control
clock = pygame.time.Clock()

# Game state variables
bird_movement = 0
score = 0
game_over = False

# Function to create pipes
def create_pipe():
    pipe_height = random.randint(100, 400)
    pipe_bottom = pygame.Rect(SCREEN_WIDTH, pipe_height, pipe_width, SCREEN_HEIGHT - pipe_height)
    pipe_top = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, pipe_height - PIPE_GAP)
    return pipe_top, pipe_bottom

# Function to check collision
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    return False

# Function to draw pipes
def draw_pipes(pipes):
    for pipe_pair in pipes:
        pygame.draw.rect(SCREEN, GREEN if pipe_pair[1].bottom >= SCREEN_HEIGHT else BLUE, pipe_pair[0])
        pygame.draw.rect(SCREEN, GREEN, pipe_pair[1])

# Function to move pipes
def move_pipes(pipes):
    for pipe_pair in pipes:
        pipe_pair[0].x -= PIPE_SPEED  # Move the top pipe
        pipe_pair[1].x -= PIPE_SPEED  # Move the bottom pipe
    return pipes

# Main game loop
def main():
    global bird_movement, score, game_over
    pipes = [create_pipe()]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_movement = BIRD_JUMP
                if event.key == pygame.K_SPACE and game_over:
                    game_over = False
                    bird_rect.center = (100, SCREEN_HEIGHT // 2)
                    pipes = [create_pipe()]
                    bird_movement = 0
                    score = 0

        if not game_over:
            # Bird movement
            bird_movement += GRAVITY
            bird_rect.centery += bird_movement

            # Pipe movement
            pipes = move_pipes(pipes)

            # Add new pipe when needed
            if pipes[-1][0].x < SCREEN_WIDTH // 2:
                pipes.append(create_pipe())

            # Remove pipes that have moved off screen
            if pipes[0][0].x < -pipe_width:
                pipes.pop(0)
                score += 1

            # Check for collisions
            if check_collision(pipes):
                game_over = True  # Stop the game if a collision occurs

        # Drawing everything
        SCREEN.fill(WHITE)
        SCREEN.blit(bird_img, bird_rect)
        draw_pipes(pipes)

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))

        # End game if collision occurs
        if game_over:
            # Render "Game Over!" text
            game_over_text1 = game_over_font.render("              Game Over!", True, (255, 0, 0))
            # Render "Press Space to Restart" text
            game_over_text2 = font.render("                   Press Space to Restart", True, BLACK)
            
            # Display the first line at a specific position
            SCREEN.blit(game_over_text1, (50, SCREEN_HEIGHT // 2))
            # Display the second line just below the first line
            SCREEN.blit(game_over_text2, (50, (SCREEN_HEIGHT // 2) + 40))  # Adjust 40 pixels lower

        # Update screen and tick clock
        pygame.display.update()
        clock.tick(60)

# Run the game
main()
