import pygame
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()  # Lade das Bild und behalte den Alpha-Kanal
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, dt):
        # Update-Logik des Spielers
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
