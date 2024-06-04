import pygame
import os

class Obstacle:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = pygame.image.load(os.path.join('assets', 'images', image_path)).convert_alpha()

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
