import pygame
from constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Initialize clock here, before the game loop
    clock = pygame.time.Clock()
    dt = 0

    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    running = True
    while running:
        for event in pygame.event.get():
            pass  # handle your events here
            
        # Draw your game here
        
        pygame.display.flip()
        
        # Control frame rate and get delta time at the end of each loop
        dt = clock.tick(60) / 1000
        
    pygame.quit()

if __name__ == "__main__":
    main()