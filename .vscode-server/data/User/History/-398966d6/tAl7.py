import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from gameinfo import GameInfo


def display_game_over(screen, font):
    """
    Zeigt den Game-Over-Bildschirm mit Restart- und Exit-Optionen an.
    """
    # Haupttext
    text = font.render("GAME OVER", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)

    # Kleineren Text für die Hinweise
    small_font = pygame.font.Font(None, 36)
    restart_text = small_font.render("Press ENTER to restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 70))
    screen.blit(restart_text, restart_rect)

    exit_text = small_font.render("Press ESC to quit", True, (255, 255, 255))
    exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120))
    screen.blit(exit_text, exit_rect)

    pygame.display.flip()


def main():
    """
    Hauptspielschleife für das Asteroidenspiel.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids!")
    clock = pygame.time.Clock()

    # Sprite-Gruppen für die Organisation von Objekten
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Container-Initialisierung
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Player.containers = (updatable, drawable)

    # Fonts und Spielinfo
    font = pygame.font.Font(None, 72)
    small_font = pygame.font.Font(None, 36)
    game_info = GameInfo()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0
    start_ticks = pygame.time.get_ticks()  # Startzeit des Spiels

    # Spielschleife
    while True:
        # Hauptspiel, solange Leben verfügbar sind
        while game_info.lives > 0:
            # Event-Verarbeitung
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update aller Objekte (Spieler, Schüsse, Asteroidenfeld, etc.)
            updatable.update(dt)

            # Überprüfung auf Kollision zwischen Spieler und Asteroiden
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    game_info.lose_life()
                    if game_info.lives > 0:
                        player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Spieler neu positionieren
                        pygame.time.wait(500)  # Kurze Pause nach Kollision
                    else:
                        break

            # Überprüfung auf Kollision zwischen Schüssen und Asteroiden
            for shot in shots:
                for asteroid in asteroids:
                    if asteroid.collides_with(shot):
                        asteroid.split()
                        shot.kill()
                        game_info.add_score(10)

            # Bildschirm aktualisieren
            screen.fill("black")
            for obj in drawable:
                obj.draw(screen)

            # HUD-Informationen anzeigen (Zeit, Punkte, Leben)
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            minutes, seconds = divmod(elapsed_time, 60)
            timer_text = small_font.render(f"Time: {int(minutes)}:{int(seconds):02d}", True, (255, 255, 255))
            score_text = small_font.render(f"Score: {game_info.score}", True, (255, 255, 255))
            lives_text = small_font.render(f"Lives: {game_info.lives}", True, (255, 255, 255))
            screen.blit(timer_text, (10, 10))
            screen.blit(score_text, (10, 40))
            screen.blit(lives_text, (10, 70))

            pygame.display.flip()
            dt = clock.tick(60) / 1000  # Zeitdifferenz seit dem letzten Frame (in Sekunden)

        # Game-Over-Bildschirm anzeigen
        display_game_over(screen, font)

        # Auf Eingaben nach dem Game-Over-Bildschirm warten
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Spiel neu starten
                        game_info.reset()
                        player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        start_ticks = pygame.time.get_ticks()  # Startzeit zurücksetzen
                        waiting_for_input = False
                    elif event.key == pygame.K_ESCAPE:  # Spiel beenden
                        pygame.quit()
                        sys.exit()


if __name__ == "__main__":
    main()
