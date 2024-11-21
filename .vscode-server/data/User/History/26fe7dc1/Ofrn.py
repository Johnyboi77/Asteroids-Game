import pygame
from constants import *

def main():
    # Initialize Pygame
    pygame.init()

    # Creating the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Printing to the console
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Here, you might want to add the game loop in future lessons

if __name__ == "__main__":
    main()