import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from gameinfo import GameInfo

def display_game_over(screen, font):
    # Anzeigen des Game-Over-Textes
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

def handle_collision_with_player(player, asteroids, game_info, screen, small_font):
    # Überprüfung auf Kollision zwischen Spieler und Asteroiden
    for asteroid in asteroids:
        if asteroid.collides_with(player):
            print("Collision detected!")  # Debug-Ausgabe
            game_info.lose_life()  # Spieler verliert ein Leben
            print(f"Lives after collision: {game_info.lives}")  # Debug-Ausgabe der verbleibenden Leben

            if game_info.lives > 0:
                # Spieler verliert ein Leben, aber das Spiel geht weiter
                player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Spieler wird neu positioniert
                pygame.time.wait(1000)  # Kurze Pause, um Kollision zu verarbeiten
            else:
                # Alle Leben verloren: Zeige "Game Over"-Bildschirm
                display_game_over(screen, small_font)
                return True  # Signalisiert, dass das Spiel vorbei ist
    return False

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
    start_ticks = pygame.time.get_ticks()  # Zeitstempel für den Start des Spiels

    # Hauptspiel-Schleife
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if game_info.lives > 0:
            # Lebensverwaltung und Kollisionserkennung
            game_over = handle_collision_with_player(player, asteroids, game_info, screen, small_font)
            if game_over:
                break  # Bricht aus der aktuellen Lebensschleife aus, um "Game Over" zu verarbeiten

            # Kollisionserkennung zwischen Schüssen und Asteroiden
            for shot in shots:
                for asteroid in asteroids:
                    if asteroid.collides_with(shot):
                        asteroid.split()
                        shot.kill()
                        game_info.add_score(10)

            # Bildschirmaktualisierung
            screen.fill("black")
            for obj in drawable:
                obj.draw(screen)

            # HUD (Zeit, Punkte, Leben)
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Zeit in Sekunden
            minutes, seconds = divmod(elapsed_time, 60)
            timer_text = small_font.render(f"Time: {int(minutes)}:{int(seconds):02d}", True, (255, 255, 255))
            score_text = small_font.render(f"Score: {game_info.score}", True, (255, 255, 255))
            lives_text = small_font.render(f"Lives: {game_info.lives}", True, (255, 255, 255))
            screen.blit(timer_text, (10, 10))
            screen.blit(score_text, (10, 40))
            screen.blit(lives_text, (10, 70))
            pygame.display.flip()
            dt = clock.tick(60) / 1000
        else:
            # Spiel ist vorbei, Leben = 0
            print("Lives: 0 - Game Over")
            display_game_over(screen, font)

            # Warten auf Eingabe für Neustart oder Beenden
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # Neustart
                            game_info.reset()
                            player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                            # Zurücksetzen von Asteroiden und Schüssen
                            asteroids.empty()
                            shots.empty()
                            AsteroidField()
                            start_ticks = pygame.time.get_ticks()  # Setze Spielzeit zurück
                            waiting_for_input = False
                        elif event.key == pygame.K_ESCAPE:  # Beenden
                            pygame.quit()
                            sys.exit()

if __name__ == "__main__":
    main()
