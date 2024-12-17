import pygame 

class GameInfo:
    def __init__(self):
        self.score = 0
        self.lives = 3  # Setze die anfängliche Anzahl an Leben
        self.start_time = pygame.time.get_ticks()  # Startzeit für den Timer

    def add_score(self, points):
        self.score += points

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    def get_elapsed_time(self):
        return (pygame.time.get_ticks() - self.start_time) / 1000  # Zeit in Sekunden

    def reset(self):
        self.score = 0
        self.lives = 3
        self.start_time = pygame.time.get_ticks()


