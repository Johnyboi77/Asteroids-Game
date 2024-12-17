import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot
from gameinfo import GameInfo

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        
        # Invincibility attributes
        self.invincible = False  # Player is not invincible initially
        self.invincible_time = 0  # How much time the player has left being invincible

    def draw(self, screen):
        # If the player is invincible, change opacity or make them blink
        if self.invincible:
            # Blinking effect: alternates visibility
            if int(self.invincible_time * 2) % 2 == 0:
                pygame.draw.polygon(screen, (255, 255, 255, 128), self.triangle(), 2)  # Semi-transparent
            else:
                pygame.draw.polygon(screen, "white", self.triangle(), 2)  # Full opacity
        else:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        # If invincible, reduce the invincibility time
        if self.invincible:
            self.invincible_time -= dt
            if self.invincible_time <= 0:
                self.invincible = False  # Stop being invincible when time runs out

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

    def activate_invincibility(self, duration=5):
        self.invincible = True
        self.invincible_time = duration(5)  # Set the duration of invincibility
