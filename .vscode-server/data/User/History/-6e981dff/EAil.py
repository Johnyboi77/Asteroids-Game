import pygame
from pygame.sprite import Sprite
from shot import Shot  # Importiere die Shot-Klasse, falls sie im Code verwendet wird

class Player(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Erstelle eine einfache Oberfläche für den Spieler
        self.image.fill((255, 255, 255))  # Fülle die Oberfläche mit der Farbe Weiß
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Initialisiere die Position und Rotation des Spielers
        self.position = pygame.Vector2(x, y)
        self.rotation = 0  # Anfangs keine Rotation
        self.shoot_timer = 0  # Initialisiere den Schieß-Timer

    def update(self, dt):
        self.shoot_timer -= dt  # Verringer den Schieß-Timer basierend auf der Delta-Zeit

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)  # Bewege den Spieler rückwärts
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()  # Wenn die Leertaste gedrückt wird, schieße

        # Die rect-Position aktualisieren, wenn der Spieler sich bewegt
        self.rect.center = self.position

    def shoot(self):
        if self.shoot_timer > 0:
            return  # Wenn der Schieß-Timer noch aktiv ist, tue nichts
        self.shoot_timer = 0.5  # Beispiel-Kühlzeit für das Schießen
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * 10  # Geschwindigkeit des Schusses
        # Füge den Shot der Spielwelt hinzu (falls das im Code erforderlich ist)
        # z.B. Shot.containers.append(shot) oder eine ähnliche Logik

    def rotate(self, dt):
        self.rotation += 200 * dt  # Beispiel-Rotationsgeschwindigkeit

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)  # Bewege den Spieler basierend auf der Rotation
        self.position += forward * 200 * dt  # Geschwindigkeit des Spielers

    def draw(self, screen):
        # Zeichne den Spieler (als Beispiel ein Rechteck)
        pygame.draw.rect(screen, (255, 255, 255), self.rect)  # Weißes Quadrat als Spieler
