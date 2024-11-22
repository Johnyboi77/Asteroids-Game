import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from gameinfo import GameInfo


def display_game_over(screen, font):
    """Zeigt den GAME OVER-Bildschirm an."""
    screen.fill("black")

    # GAME OVER Nachricht
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    restart_text = font.render("Drücke Enter zum Neustarten", True, (255, 255, 255))

    # Zentriere die Texte
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))

    # Texte auf dem Bildschirm anzeigen
    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Setze Container für Asteroiden, Schüsse und das Spielfeld
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    # Setze Container für den Spieler
    Player.containers = (updatable, drawable)

    font = pygame.font.Font(None, 72)  # Große Schriftart für GAME OVER
    small_font = pygame.font.Font(None, 36)  # Kleinere Schriftart für Timer, Score etc.

    while True:  # Haupt-Spiel-Loop
        game_info = GameInfo()  # Setze das Spiel zurück
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        dt = 0

        while game_info.lives > 0:  # Innere Spiel-Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Aktualisiere alle Objekte
            for obj in updatable:
                obj.update(dt)

            # Kollisionslogik für Asteroiden und den Spieler
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    game_info.lose_life()  # Spieler verliert ein Leben
                    if game_info.lives > 0:
                        # Respawn den Spieler in der Mitte des Bildschirms
                        player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

                # Kollisionslogik für Schüsse und Asteroiden
                for shot in shots:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        asteroid.split()
                        game_info.add_score(100)  # Punkte hinzufügen

            # Bildschirm füllen
            screen.fill("black")

            # Zeichne alle Objekte
            for obj in drawable:
                obj.draw(screen)

            # Timer, Score und Leben rendern
            elapsed_time = game_info.get_elapsed_time()
            minutes, seconds = divmod(elapsed_time, 60)  # Minuten und Sekunden berechnen

            # Texte erstellen
            timer_text = small_font.render(f"Zeit: {minutes}min {seconds}s", True, (255, 255, 255))
            score_text = small_font.render(f"Punkte: {game_info.score}", True, (255, 255, 255))
            lives_text = small_font.render(f"Leben: {game_info.lives}", True, (255, 255, 255))

            # Texte auf den Bildschirm zeichnen
            screen.blit(timer_text, (10, 10))  # Timer oben links
            screen.blit(score_text, (10, 40))  # Score darunter
            screen.blit(lives_text, (10, 70))  # Leben darunter

            # Bildschirm aktualisieren
            pygame.display.flip()

            # Framerate auf 60 FPS begrenzen
            dt = clock.tick(60) / 1000

        # GAME OVER anzeigen
        display_game_over(screen, font)

        # Warte auf Enter, um neu zu starten
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    break  # Spiel neu starten
            else:
                continue  # Bleibe in der Schleife, wenn Enter nicht gedrückt wurde
            break


if __name__ == "__main__":
    main()

