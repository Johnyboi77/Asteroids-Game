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

def reset_game(updatable, drawable, asteroids, shots, player, game_info):
    asteroids.empty()
    shots.empty()
    player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    game_info.reset()
    for _ in range(5): 
        asteroid = Asteroid()
        asteroids.add(asteroid)
        updatable.add(asteroid)
        drawable.add(asteroid)

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
    collision_cooldown = 0  # Zeitstempel für Kollision

    # Hauptspiel-Schleife
    while True:
        # Spiel läuft, solange der Spieler Leben hat
        while game_info.lives > 0:
            current_time = pygame.time.get_ticks()  # Aktuelle Zeit abrufen
            if game_info.lives == 3:
                print("3 lives remaining")
            elif game_info.lives == 2:
                print("2 lives remaining")
            elif game_info.lives == 1:
                print("1 life remaining")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Nur aktualisieren, wenn keine Kollisionsverzögerung aktiv ist
            if current_time > collision_cooldown:
                for obj in updatable:
                    obj.update(dt)

                # Überprüfung auf Kollision zwischen Spieler und Asteroiden
                for asteroid in asteroids:
                    if asteroid.collides_with(player):
                        print("Collision detected!")  # Debug: Kollision erkannt
                        game_info.lose_life()  # Leben abziehen
                        print(f"Lives after collision: {game_info.lives}")  # Debug: Leben nach Abzug
                        if game_info.lives > 0:
                            print(f"{game_info.lives} lives remaining. Keep going!")  # Debug
                            player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Spieler neu positionieren
                            collision_cooldown = current_time + 1000  # 1 Sekunde Verzögerung
                        else:
                            print("No lives remaining. Game Over!")  # Debug
                            break

            # Überprüfung auf Kollision zwischen Schüssen und Asteroiden
            for shot in shots:
                for asteroid in asteroids:
                    if asteroid.collides_with(shot):
                        asteroid.split()
                        shot.kill()
                        game_info.add_score(10)

            # Bildschirm zeichnen
            screen.fill("black")
            for obj in drawable:
                obj.draw(screen)

            # HUD (Punkte, Zeit, Leben)
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # in Sekunden
            minutes, seconds = divmod(elapsed_time, 60)
            timer_text = small_font.render(f"Time: {int(minutes)}:{int(seconds):02d}", True, (255, 255, 255))  # Formatierte Zeit
            score_text = small_font.render(f"Score: {game_info.score}", True, (255, 255, 255))
            lives_text = small_font.render(f"Lives: {game_info.lives}", True, (255, 255, 255))
            screen.blit(timer_text, (10, 10))
            screen.blit(score_text, (10, 40))
            screen.blit(lives_text, (10, 70))
            pygame.display.flip()
            dt = clock.tick(60) / 1000

        # Wenn die Leben auf 0 fallen
        print("Lives: 0 - Game Over")
        display_game_over(screen, font)

        waiting_for_input = True

        while waiting_for_input:
            for event in pygame.event.get():
                # Das Schließen des Spiels nur bei QUIT Event, aber nicht bei RETURN oder ESC
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Spiel neu starten
                        reset_game(updatable, drawable, asteroids, shots, player, game_info, asteroid_field)
                        start_ticks = pygame.time.get_ticks()  # Setze die Startzeit zurück
                        waiting_for_input = False  # Verlasse die Eingabewarteschleife
                    elif event.key == pygame.K_ESCAPE:  # Spiel beenden
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()