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

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Player.containers = (updatable, drawable)

    font = pygame.font.Font(None, 72)
    small_font = pygame.font.Font(None, 36)
    game_info = GameInfo()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0
    while True:
        while game_info.lives > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            for obj in updatable:
                obj.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    if not player.invincible:
                        game_info.lose_life()
                        player.activate_invincibility(duration=3)  # Unverwundbarkeit aktivieren
                    if game_info.lives > 0:
                # Spieler neu positionieren, das Spiel läuft weiter
                        player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    else:
                # Spieler hat keine Leben mehr, Schleife verlassen
                        game_info.lives = 0
                        break

            for shot in shots:
                for asteroid in asteroids:
                    if asteroid.collides_with(shot):
                        asteroid.split()
                        shot.kill()
                        game_info.add_score(10)

            screen.fill("black")
            for obj in drawable:
                obj.draw(screen)

            elapsed_time = game_info.get_elapsed_time()
            minutes, seconds = divmod(elapsed_time, 60)
            timer_text = small_font.render(f"Time: {minutes}min {seconds}s", True, (255, 255, 255))
            score_text = small_font.render(f"Score: {game_info.score}", True, (255, 255, 255))
            lives_text = small_font.render(f"Lives: {game_info.lives}", True, (255, 255, 255))
            screen.blit(timer_text, (10, 10))
            screen.blit(score_text, (10, 40))
            screen.blit(lives_text, (10, 70))
            pygame.display.flip()
            dt = clock.tick(60) / 1000

        display_game_over(screen, font)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_info.reset()
                    break
            else:
                continue
            break

if __name__ == "__main__":
    main()