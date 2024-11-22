import time

class GameInfo:
    def __init__(self):
        self.start_time = time.time()
        self.score = 0

    def get_elapsed_time(self):
        return int(time.time() - self.start_time)

    def add_score(self, points):
        self.score += points

    def reset(self):
        self.start_time = time.time()
        self.score = 0

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    def reset(self):
        self.start_time = time.time()
        self.score = 0
        self.lives = 3
