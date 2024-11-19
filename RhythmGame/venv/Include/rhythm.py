import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Rhythm Game")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (RGB: Blue)
    screen.fill((0, 0, 255))

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
