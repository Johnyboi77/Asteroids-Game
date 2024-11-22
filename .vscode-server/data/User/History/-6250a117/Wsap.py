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

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    game_info = GameInfo()
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                sys.exit()

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
                    game_info.add_score(100)

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

                # Timer und Score rendern
        font = pygame.font.Font(None, 36)  # Wähle eine Schriftart und Größe
        elapsed_time = game_info.get_elapsed_time()
        timer_text = font.render(f"Zeit: {elapsed_time}s", True, (255, 255, 255))
        score_text = font.render(f"Punkte: {game_info.score}", True, (255, 255, 255))

        # Zeichne Timer und Score
        screen.blit(timer_text, (10, 10))  # Timer oben links
        screen.blit(score_text, (10, 40))  # Score direkt darunter

        # Bildschirm aktualisieren
        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()