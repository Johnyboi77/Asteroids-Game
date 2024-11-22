import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from gameinfo import GameInfo

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set containers for asteroids, shots, and asteroid field
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    # Set container for player
    Player.containers = (updatable, drawable)

    font = pygame.font.Font(None, 72)  # Large font for "GAME OVER"
    small_font = pygame.font.Font(None, 36)  # Smaller font for timer, score, etc.

    game_info = GameInfo()  # Initialize the game info object
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0
    while True:  # Main game loop
        while game_info.lives > 0:  # Main game loop only runs when lives are left
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update all objects
            for obj in updatable:
                obj.update(dt)

            # Handle collisions between player and asteroids
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    if not player.invincible:  # Only lose a life if the player is not invincible
                        game_info.lose_life()  # Player loses a life
                        player.activate_invincibility()  # Activate invincibility for a few seconds
                        if game_info.lives > 0:
                            player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Respawn the player

                            # Print the remaining lives
                            if game_info.lives == 1:
                                print(f"Life lost, 1 Life remaining")
                            else:
                                print(f"Life lost, {game_info.lives} Lives remaining")

            # Fill the screen with black
            screen.fill("black")

            # Draw all objects
            for obj in drawable:
                obj.draw(screen)

            # Timer, score, and lives display
            elapsed_time = game_info.get_elapsed_time()
            minutes, seconds = divmod(elapsed_time, 60)  # Calculate minutes and seconds

            # Render text
            timer_text = small_font.render(f"Time: {minutes}min {seconds}s", True, (255, 255, 255))
            score_text = small_font.render(f"Score: {game_info.score}", True, (255, 255, 255))
            lives_text = small_font.render(f"Lives: {game_info.lives}", True, (255, 255, 255))

            # Draw the text on the screen
            screen.blit(timer_text, (10, 10))  # Timer in top left
            screen.blit(score_text, (10, 40))  # Score below timer
            screen.blit(lives_text, (10, 70))  # Lives below score

            # Update the screen
            pygame.display.flip()

            # Limit the framerate to 60 FPS
            dt = clock.tick(60) / 1000

        # GAME OVER screen
        display_game_over(screen, font)

        # Wait for 'Enter' to restart the game
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_info.reset()  # Reset the game
                    break  # Restart the game
            else:
                continue  # Stay in the loop if 'Enter' wasn't pressed
            break

if __name__ == "__main__":
    main()