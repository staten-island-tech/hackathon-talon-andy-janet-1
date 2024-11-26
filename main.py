import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 853
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Blue color for one of the blocks
GREEN = (0, 255, 0)  # Green color for another block
ORANGE = (255, 165, 0)  # Orange color for another block
BLACK = (0, 0, 0)

# Game Variables
note_speed = 7  # Speed of the notes
note_height = 80
score = 0
misses = 0

# Font for score and text
font = pygame.font.SysFont(None, 40)  # Adjusted font size for larger screen
title_font = pygame.font.SysFont(None, 80)  # Larger title font

# Key mappings for player input (only 4 keys: d, f, j, k)
keys = ['d', 'f', 'j', 'k']
key_map = {'d': pygame.K_d, 'f': pygame.K_f, 'j': pygame.K_j, 'k': pygame.K_k}

# Lane width (equal for all keys)
lane_width = SCREEN_WIDTH // len(keys)

# Key lane positions (evenly distributed across the screen width)
lane_positions = {
    'd': lane_width * 0,    # Lane for key D
    'f': lane_width * 1,    # Lane for key F
    'j': lane_width * 2,    # Lane for key J
    'k': lane_width * 3     # Lane for key K
}

# Load sounds for each block (Ensure these files are present in your project directory)
red_sound = pygame.mixer.Sound("red_sound.wav")   # Replace with actual file paths
blue_sound = pygame.mixer.Sound("blue_sound.wav") 
orange_sound = pygame.mixer.Sound("orange_sound.wav") 
green_sound = pygame.mixer.Sound("green_sound.wav") 

# Load background music (make sure this file exists)
pygame.mixer.music.load("megalovania.mp3")  # Replace with the path to your music file

# Define the Note class
class Note:
    def __init__(self, key, y, color, sound):
        self.key = key
        self.x = lane_positions[key] + lane_width // 2  # Center the note within the lane
        self.y = y
        self.rect = pygame.Rect(self.x - lane_width // 4, self.y, lane_width // 2, note_height)  # Adjusted width for block
        self.color = color  # Color for the note (Red, Blue, Orange, Green)
        self.sound = sound  # Sound associated with the note
    
    def move(self):
        self.y += note_speed
        self.rect.y = self.y
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Function to display score and misses
def display_score():
    score_text = font.render(f"Score: {score}  Misses: {misses}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to display the starting screen with blinking text and a pattern background
def show_start_screen():
    screen.fill(BLACK)  # Fill screen with black to clear it
    draw_pattern()  # Draw the background pattern
    draw_blinking_stars()  # Draw random blinking stars
    
    title_text = title_font.render("Rhythm Game", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    
    # Blinking effect for "Press SPACE to Start"
    global last_blink_time, blink_state
    if time.time() - last_blink_time > 0.5:
        last_blink_time = time.time()
        blink_state = not blink_state  # Toggle visibility

    if blink_state:
        # Display title and instructions
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
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
    hit_zone_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100, 20)  # Hit zone (adjusted size)
    pygame.draw.rect(screen, WHITE, hit_zone_rect, 2)  # Draw a white rectangle as the hit zone

# Function to draw the separation lines between lanes
def draw_separation_lines():
    for i in range(1, len(keys)):  # Create separation lines between the keys
        pygame.draw.line(screen, WHITE, (lane_positions[keys[i]] - lane_width // 2, 0),
                         (lane_positions[keys[i]] - lane_width // 2, SCREEN_HEIGHT), 2)

# Function to draw the background pattern (random blinking stars)
def draw_pattern():
    for y in range(0, SCREEN_HEIGHT, 40):
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(screen, WHITE, (x, y), (x + 20, y + 20), 1)  # Diagonal lines

# Function to draw random blinking stars
def draw_blinking_stars():
    current_time = time.time()
    for i in range(10):  # Draw 10 random stars
        star_x = random.randint(0, SCREEN_WIDTH)
        star_y = random.randint(0, SCREEN_HEIGHT)
        star_size = random.randint(1, 3)  # Small stars
        
        # Only draw the star if it's within the blink period (5 seconds)
        if current_time % 5 < 2.5:  # Make stars blink every 5 seconds
            pygame.draw.circle(screen, WHITE, (star_x, star_y), star_size)

# Main Game Loop
def game_loop():
    global score, misses
    running = True
    clock = pygame.time.Clock()
    notes = []
    last_red_time = time.time()
    last_blue_time = time.time()
    last_orange_time = time.time()
    last_green_time = time.time()

    # Colors for notes: Red, Blue, Orange, Green
    note_colors = {
        'red': RED,
        'blue': BLUE,
        'orange': ORANGE,
        'green': GREEN
    }

    # Track next random times for notes
    next_red_time = random.uniform(0.5, 2)
    next_blue_time = random.uniform(1, 3)
    next_orange_time = random.uniform(1.5, 4)
    next_green_time = random.uniform(1.5, 2)
    
    # Play background music in a loop
    pygame.mixer.music.play(loops=-1, start=0.0)

    while running:
        screen.fill(BLACK)  # Fill screen with black to clear it
        draw_pattern()  # Draw the background pattern
        draw_blinking_stars()  # Draw random blinking stars
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Key press event handling
            if event.type == pygame.KEYDOWN:
                for note in notes:
                    if event.key == key_map[note.key] and note.rect.colliderect(pygame.Rect(50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100, 20)):
                        score += 1
                        note.sound.play()  # Play the corresponding sound for the note
                        notes.remove(note)
                        break
                else:
                    misses += 1  # Missed the note

        # Generate notes at random intervals
        current_time = time.time()

        if current_time - last_red_time > next_red_time:
            notes.append(Note('d', 0, RED, red_sound))  # Red block
            last_red_time = current_time
            next_red_time = random.uniform(0.5, 2)  # Set new random time for next Red note

        if current_time - last_blue_time > next_blue_time:
            notes.append(Note('f', 0, BLUE, blue_sound))  # Blue block
            last_blue_time = current_time
            next_blue_time = random.uniform(1, 3)  # Set new random time for next Blue note

        if current_time - last_orange_time > next_orange_time:
            notes.append(Note('j', 0, ORANGE, orange_sound))  # Orange block
            last_orange_time = current_time
            next_orange_time = random.uniform(1.5, 4)  # Set new random time for next Orange note

        if current_time - last_green_time > next_green_time:
            notes.append(Note('k', 0, GREEN, green_sound))  # Green block
            last_green_time = current_time
            next_green_time = random.uniform(1.5, 2)  # Set new random time for next Green note

        # Move and draw notes
        for note in notes[:]:
            note.move()
            note.draw()
            if note.y > SCREEN_HEIGHT:  # If note goes off screen
                notes.remove(note)
                misses += 1

        # Draw separation lines for lanes
        draw_separation_lines()

        # Draw the hit zone bar at the bottom
        draw_hit_zone()

        # Display score and misses
        display_score()

        # Draw the key labels at the bottom (d, f, j, k)
        draw_key_labels()

        pygame.display.update()  # Update the screen
        clock.tick(60)  # Cap the frame rate to 60 FPS

    pygame.quit()

# Function to display the key labels at the bottom of the screen (d, f, j, k)
def draw_key_labels():
    for i, key in enumerate(keys):
        key_text = font.render(key.upper(), True, WHITE)
        x_pos = lane_positions[key] + lane_width // 2 - key_text.get_width() // 2
        screen.blit(key_text, (x_pos, SCREEN_HEIGHT - 60))  # Position it near the bottom of the screen

# Initialize blinking variables
last_blink_time = time.time()
blink_state = True

# Show the start screen and start the game
show_start_screen()
game_loop()

# Quit Pygame
pygame.quit()
quit()
