import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.alpha_value = 255  # Standard-Alpha-Wert (volle Deckkraft)

    def triangle(self):
        """
        Gibt die Koordinaten eines Dreiecks zurück, das das Raumschiff des Spielers darstellt.
        """
        x = self.position.x
        y = self.position.y
        size = PLAYER_RADIUS  # Größe des Raumschiffs (Dreieck)
        
        # Die drei Punkte des Dreiecks
        points = [
            (x, y - size),  # Spitze des Dreiecks
            (x - size, y + size),  # Untere linke Ecke
            (x + size, y + size)   # Untere rechte Ecke
        ]
        return points

    def draw(self, screen):
        # Setze den Alpha-Wert auf die gewünschte Sichtbarkeit
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        # Zeichne das Raumschiff (Dreieck) mit dem aktuellen Alpha-Wert
        pygame.draw.polygon(surface, (255, 255, 255, self.alpha_value), self.triangle(), 0)
        
        # Zeichne die Oberfläche auf den Bildschirm
        screen.blit(surface, (self.position.x - self.radius, self.position.y - self.radius))

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
