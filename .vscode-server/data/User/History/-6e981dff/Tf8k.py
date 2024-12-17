import pygame
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Erstelle eine einfache Oberfläche für den Spieler
        self.image.fill((255, 255, 255))  # Fülle die Oberfläche mit der Farbe Weiß
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, dt):
        # Update-Logik des Spielers
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Die rect-Position aktualisieren, wenn der Spieler sich bewegt
        self.rect.center = self.position

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt