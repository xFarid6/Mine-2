import math
import pygame
import random

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20

        self.white = (255, 255, 255)
        self.purple = (128, 0, 128)
        self.thickness = 0
        self.highlighted = False

        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.lastx = self.x
        self.lasty = self.y
        self.accx = 0
        self.accy = 0
        self.gravity = (-0.1, 1.0)

    def set_higlihted(self, highlighted):
        self.highlighted = highlighted

    def move(self):
        velocityx = (self.x - self.lastx) * 0.95
        velocityy = (self.y - self.lasty) * 0.95

        self.lastx = self.x
        self.lasty = self.y

        self.x += velocityx + self.accx * 0.4
        self.y += velocityy + self.accy * 0.4

        self.accx = 0
        self.accy = 0

    def apply_force(self, force):
        self.accx += force[0]
        self.accy += force[1]

    def constraints(self):
        if self.x + self.radius > self.screen_width:
            self.x = self.screen_width - self.radius
        elif self.x - self.radius < 0:
            self.x = self.radius
        
        if self.y + self.radius > self.screen_height:
            self.y = self.screen_height - self.radius
        elif self.y - self.radius < 0:
            self.y = self.radius

    def constraints_C(self):
        center: pygame.math.Vector2 = pygame.math.Vector2(self.screen_width / 2, self.screen_height / 2)
        radius = 300
        to_object: pygame.math.Vector2 = pygame.math.Vector2(self.x, self.y) - center
        distance = to_object.length() # x**2 + y**2 = r**2
        if distance > radius - self.radius:
            n = to_object.normalize() # to_object / x**2 + y**2 = 1
            curr_pos = center + n * (radius - self.radius)
            self.x = curr_pos.x # - .45
            self.y = curr_pos.y

    def draw(self):
        pygame.draw.circle(self.screen, self.white, (self.x, self.y), self.radius, self.thickness)
        if self.highlighted:
            pygame.draw.circle(self.screen, self.purple, (self.x, self.y), self.radius, 4)

    def intersects(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 < (self.radius + other.radius) ** 2

    def verlet(self, other):
        #collision axis
        x = self.x - other.x
        y = self.y - other.y

        # distance
        distance = math.pow((math.pow(x, 2) + math.pow(y, 2)), 0.5)
        if distance == 0:
            return

        # normal
        nx = x / distance
        ny = y / distance

        # delta
        delta = (self.radius + other.radius) - distance

        # update position
        self.x += nx * delta * 0.5
        self.y += ny * delta * 0.5
