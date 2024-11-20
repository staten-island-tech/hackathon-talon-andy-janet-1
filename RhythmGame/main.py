import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Game Variables
note_speed = 5
note_width = 50
note_height = 30
note_gap = 100  # Space between falling notes
score = 0
misses = 0

# Font for score and text
font = pygame.font.SysFont(None, 30)
title_font = pygame.font.SysFont(None, 60)

# Key mappings for player input
keys = ['left', 'right', 'space']  # Corresponding to different notes
key_map = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'space': pygame.K_SPACE}

# Define the Note class
class Note:
    def __init__(self, key, y):
        self.key = key
        self.x = random.randint(100, SCREEN_WIDTH - note_width - 100)  # Random horizontal position
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, note_width, note_height)
    
    def move(self):
        self.y += note_speed
        self.rect.y = self.y
    
    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# Function to display score and misses
def display_score():
    score_text = font.render(f"Score: {score}  Misses: {misses}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to display the starting screen
def show_start_screen():
    screen.fill(BLACK)  # Fill screen with black to clear it
    title_text = title_font.render("Rhythm Game", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    
    # Display title and instructions
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    
    pygame.display.update()

    # Wait for the player to press space to start
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False  # Start the game when space is pressed

# Main Game Loop
def game_loop():
    global score, misses
    running = True
    clock = pygame.time.Clock()
    notes = []
    note_interval = 1  # Interval at which notes spawn
    last_note_time = time.time()

    while running:
        screen.fill(BLACK)  # Fill screen with black to clear it

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Key press event handling
            if event.type == pygame.KEYDOWN:
                for note in notes:
                    if event.key == key_map[note.key] and note.rect.colliderect(pygame.Rect(100, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 200, 10)):
                        # Check if key press is within the "hit zone"
                        score += 1
                        notes.remove(note)
                        break
                else:
                    misses += 1  # Missed the note

        # Generate notes at intervals
        if time.time() - last_note_time > note_interval:
            new_note = Note(random.choice(keys), 0)  # Create a new note with a random key
            notes.append(new_note)
            last_note_time = time.time()

        # Move and draw notes
        for note in notes[:]:
            note.move()
            note.draw()
            if note.y > SCREEN_HEIGHT:  # If note goes off screen
                notes.remove(note)
                misses += 1

        # Display score and misses
        display_score()

        pygame.display.update()  # Update the screen
        clock.tick(60)  # Cap the frame rate to 60 FPS

    pygame.quit()

# Run the starting screen first
show_start_screen()

# Run the game loop after the start screen
game_loop()
