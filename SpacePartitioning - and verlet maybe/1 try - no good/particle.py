import pygame
from settings import *


class Particle:

    img = pygame.image.load(r"C:\Cose Nuove\Code\Mine 2\SpacePartitioning - and verlet maybe\circle.png")
    size = img.get_width() // 20

    def __init__(self, x: int, y: int) -> None:
        self.radius = self.__class__.img.get_width() // 2
        self.color = (255, 255, 255)
        self.mass = 1
        
        self.x = x
        self.y = y

        self.last_x = self.x
        self.last_y = self.y

        self.acc_x = 0
        self.acc_y = 0

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.img, (self.x - self.radius, self.y - self.radius))

    def update(self) -> None:
        self.apply_gravity()
        # self.apply_friction()
        self.apply_velocity()
        self.check_bounds()

    def apply_gravity(self) -> None:
        self.y += Gravity

    def apply_friction(self) -> None:
        self.x *= Friction
        self.y *= Friction

    def apply_velocity(self) -> None:
        vel_x = self.x - self.last_x
        vel_y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        self.x += vel_x + self.acc_x
        self.y += vel_y + self.acc_y

        self.acc_x = 0
        self.acc_y = 0

    def check_bounds(self) -> None:
        if self.x - self.radius < 0:
            self.x = self.radius
        elif self.x + self.radius > Width:
            self.x = Width - self.radius

        if self.y - self.radius < 0:
            self.y = self.radius
        elif self.y + self.radius > Height:
            self.y = Height - self.radius

    def distance(self, particle) -> float:
        return ((self.x - particle.x) ** 2 + (self.y - particle.y) ** 2) ** 0.5