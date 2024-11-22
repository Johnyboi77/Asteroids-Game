import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from gameinfo import GameInfo


def display_game_over(screen, font):
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.fill("black")
    screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2, SCREEN_HEIGHT / 2 - game_over_text.get_height() / 2))
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set containers for asteroids, shots, and the asteroid field
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    # Set container for the player
    Player.containers = (updatable, drawable)

    font = pygame.font.Font(None, 72)  # Large font for GAME OVER
    small_font = pygame.font.Font(None, 36)  # Smaller font for timer, score, etc.

    while True:  # Main game loop
        game_info = GameInfo()  # Reset the game
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        dt = 0

        while game_info.lives > 0:  # Inner game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update all objects
            for obj in updatable:
                obj.update(dt)

            # Collision logic for asteroids and the player
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    if not player.invincible:  # Only lose a life if not invincible
                        game_info.lose_life()  # Player loses a life
                        player.activate_invincibility()  # Activate invincibility
                        if game_info.lives > 0:
                            # Respawn the player in the middle of the screen
                            player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

                            # Print life lost message
                            if game_info.lives == 1:
                                print(f"Life lost, 1 Life remaining")
                            else:
                                print(f"{game_info.lives} Lives remaining")

            # Collision logic for shots and asteroids
            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
                    game_info.add_score(100)  # Add points

            # Fill the screen
            screen.fill("black")

            # Draw all objects
            for obj in drawable:
                obj.draw(screen)

            # Render timer, score, and lives
            elapsed_time = game_info.get_elapsed_time()
            minutes, seconds = divmod(int(elapsed_time), 60)  # Convert to full seconds

            # Create texts
            timer_text = small_font.render(f"Time: {minutes}min {seconds}s", True, (255, 255, 255))
            score_text = small_font.render(f"Score: {game_info.score}", True, (255, 255, 255))
            lives_text = small_font.render(f"Lives: {game_info.lives}", True, (255, 255, 255))

            # Draw texts on the screen
            screen.blit(timer_text, (10, 10))  # Timer at the top left
            screen.blit(score_text, (10, 40))  # Score below the timer
            screen.blit(lives_text, (10, 70))  # Lives below the score

            # Update the screen
            pygame.display.flip()

            # Limit the framerate to 60 FPS
            dt = clock.tick(60) / 1000

        # Show GAME OVER screen when the player has no lives left
        display_game_over(screen, font)

        # Wait for Enter to restart
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_info.reset()  # Reset the game
                    break  # Restart the game
            else:
                continue  # Stay in the loop if Enter was not pressed
            break  # Exit the loop when Enter is pressed


if __name__ == "__main__":
    main()