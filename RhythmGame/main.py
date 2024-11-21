import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game Variables
note_speed = 5
note_width = 80  # Size of notes
note_height = 60  # Size of notes
note_gap = 100  # Space between falling notes
score = 0
misses = 0
hold_blocks = []  # List of hold blocks that the player must hold down to hit
holding = False  # Whether the player is holding down a key
hold_duration = 0  # Duration of time for the hold block to register

# Font for score and text
font = pygame.font.SysFont(None, 30)
title_font = pygame.font.SysFont(None, 60)

# Key mappings for player input
keys = ['d', 'f', 'space', 'j', 'k']  # Add space as a key
key_map = {'d': pygame.K_d, 'f': pygame.K_f, 'space': pygame.K_SPACE, 'j': pygame.K_j, 'k': pygame.K_k}

# Key lane positions (x positions) - adding space in the middle
lane_positions = {
    'd': 100,  # Lane for key D
    'f': 200,  # Lane for key F
    'space': 350,  # Lane for space key
    'j': 500,  # Lane for key J
    'k': 600   # Lane for key K
}

# Define the Note class
class Note:
    def __init__(self, key, y, is_hold=False):
        self.key = key
        self.x = lane_positions[key]  # Set the x position based on the key's lane
        self.y = y
        self.rect = pygame.Rect(self.x - note_width // 2, self.y, note_width, note_height)
        self.is_hold = is_hold  # Whether this note is a hold block
    
    def move(self):
        self.y += note_speed
        self.rect.y = self.y
    
    def draw(self):
        color = RED if not self.is_hold else (255, 165, 0)  # Different color for hold blocks
        pygame.draw.rect(screen, color, self.rect)

# Function to display score and misses
def display_score():
    score_text = font.render(f"Score: {score}  Misses: {misses}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to display the starting screen with blinking text
def show_start_screen():
    screen.fill(BLACK)  # Fill screen with black to clear it
    title_text = title_font.render("Rhythm Game", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    
    # Blinking effect for "Press SPACE to Start"
    global last_blink_time, blink_state
    if time.time() - last_blink_time > 0.5:
        last_blink_time = time.time()
        blink_state = not blink_state  # Toggle visibility

    if blink_state:
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

# Function to display the hit zone bar at the bottom
def draw_hit_zone():
    hit_zone_rect = pygame.Rect(50, SCREEN_HEIGHT - 60, SCREEN_WIDTH - 100, 10)  # Hit zone
    pygame.draw.rect(screen, WHITE, hit_zone_rect, 2)  # Draw a white rectangle as the hit zone

# Function to display the visual blocks for keys (D, F, Space, J, K) covering the lanes
def draw_key_blocks():
    key_block_width = 100
    key_block_height = 30
    for key, x in lane_positions.items():
        pygame.draw.rect(screen, GREEN, pygame.Rect(x - key_block_width // 2, SCREEN_HEIGHT - 50, key_block_width, key_block_height))
        key_text = font.render(key.upper(), True, WHITE)
        screen.blit(key_text, (x - key_text.get_width() // 2, SCREEN_HEIGHT - 50 + (key_block_height - key_text.get_height()) // 2))

# Main Game Loop
def game_loop():
    global score, misses, holding, hold_duration
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
                    if event.key == key_map[note.key] and note.rect.colliderect(pygame.Rect(50, SCREEN_HEIGHT - 60, SCREEN_WIDTH - 100, 10)):
                        if note.is_hold:
                            holding = True
                            hold_duration = 0  # Reset hold duration for this hold block
                        else:
                            score += 1
                            notes.remove(note)
                            break
                else:
                    misses += 1  # Missed the note

            if event.type == pygame.KEYUP:
                if holding:
                    holding = False  # Stop holding if the player releases the key

        # Generate notes at intervals
        if time.time() - last_note_time > note_interval:
            is_hold = random.choice([False, True])  # Randomly decide if this is a hold block
            new_note = Note(random.choice(keys), 0, is_hold)  # Create a new note with a random key
            notes.append(new_note)
            last_note_time = time.time()

        # Move and draw notes
        for note in notes[:]:
            note.move()
            note.draw()
            if note.y > SCREEN_HEIGHT:  # If note goes off screen
                notes.remove(note)
                misses += 1

        # Draw the hit zone bar at the bottom
        draw_hit_zone()

        # Draw the key blocks at the bottom
        draw_key_blocks()

        # Display score and misses
        display_score()

        # Handle hold block logic: check if the key was held long enough
        if holding:
            hold_duration += 1
            if hold_duration > 30:  # Threshold for holding a key (adjustable)
                holding = False
                score += 1  # Successfully hit the hold block
                hold_duration = 0

        pygame.display.update()  # Update the screen
        clock.tick(60)  # Cap the frame rate to 60 FPS

    pygame.quit()

# Initialize blinking variables
last_blink_time = time.time()
blink_state = True

# Run the starting screen first
show_start_screen()

# Run the game loop after the start screen
game_loop()
