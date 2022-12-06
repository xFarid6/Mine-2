import pygame
import random

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8

        self.white = (255, 255, 255)
        self.purple = (128, 0, 128)
        self.thickness = 0
        self.screen = pygame.display.get_surface()
        self.highlighted = False

    def set_higlihted(self, highlighted):
        self.highlighted = highlighted

    def move(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

    def draw(self):
        pygame.draw.circle(self.screen, self.white, (self.x, self.y), self.radius, self.thickness)
        if self.highlighted:
            pygame.draw.circle(self.screen, self.purple, (self.x, self.y), self.radius, 4)

    def intersects(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 < (self.radius + other.radius) ** 2
