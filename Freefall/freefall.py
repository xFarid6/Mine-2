import random
import pygame
from dataclasses import dataclass, field
from constants import BackgroundColor, Width, Height, FPS, color_codes
from chicken import Chicken
from obstacles import Obstacles
from typing import Any

class Background:
    def __init__(self):
        """A class for drawing the background"""
        self.surfaces: list[list] = []

        # each surface will be transparent and will be drawn on top of each other
        # to create the illusion of depth
        # each will only contain one drawn object (a circle, a rectangle, etc.)
        # which should have alpha channel set to 100

        surf_size = (200, 200)

        self.square = pygame.Surface(surf_size, pygame.SRCALPHA)
        self.square.fill((255, 255, 255, 100))
        self.sx, self.sy = random.randint(0, Width - surf_size[0]), random.randint(0, Height - surf_size[0])
        self.svector = [random.randint(0, 1) * 2 - 1, random.randint(0, 1) * 2 - 1]

        self.circle = pygame.Surface(surf_size, pygame.SRCALPHA)
        pygame.draw.circle(self.circle, (255, 255, 255, 100), (100, 100), 100)
        self.cx, self.cy = random.randint(0, Width - surf_size[0]), random.randint(0, Height - surf_size[0])
        self.cvector = [random.randint(0, 1) * 2 - 1, random.randint(0, 1) * 2 - 1]

        self.rectangle = pygame.Surface(surf_size, pygame.SRCALPHA)
        pygame.draw.rect(self.rectangle, (255, 255, 255, 100), (0, 0, 200, 100))
        self.rx, self.ry = random.randint(0, Width - surf_size[0]), random.randint(0, Height - surf_size[0])
        self.rvector = [random.randint(0, 1) * 2 - 1, random.randint(0, 1) * 2 - 1]

        self.triangle = pygame.Surface(surf_size, pygame.SRCALPHA)
        triangle_points = [(0, 100), (50, 0), (100, 200)]
        pygame.draw.polygon(self.triangle, (255, 255, 255, 100), triangle_points)
        self.tx, self.ty = random.randint(0, Width - surf_size[0]), random.randint(0, Height - surf_size[0])
        self.tvector = [random.randint(0, 1) * 2 - 1, random.randint(0, 1) * 2 - 1]

        self.surfaces.append([self.square, [self.sx, self.sy], self.svector])
        self.surfaces.append([self.circle, [self.cx, self.cy], self.cvector])
        self.surfaces.append([self.rectangle, [self.rx, self.ry], self.rvector])
        self.surfaces.append([self.triangle, [self.tx, self.ty], self.tvector])

    def update(self, deltaTime: float):
        for surface, pos, vector in self.surfaces:
            x, y = vector
            pos[0] += x * deltaTime * 100
            pos[1] += y * deltaTime * 100

            surface_width, surface_height = surface.get_size()
            if pos[0] + surface_width > Width or pos[0] < 0:
                vector[0] *= -1
            if pos[1] + surface_height > Height or pos[1] < 0:
                vector[1] *= -1

        if random.randint(0, 100) < 10:
            # update square color
            self.square.fill(random.choice(list(color_codes.values())))
            # update circle color
            pygame.draw.circle(self.circle, random.choice(list(color_codes.values())), (100, 100), 100)
            # update rectangle color
            pygame.draw.rect(self.rectangle, random.choice(list(color_codes.values())), (0, 0, 200, 100))
            # update triangle color
            triangle_points = [(0, 100), (50, 0), (100, 200)]
            pygame.draw.polygon(self.triangle, random.choice(list(color_codes.values())), triangle_points)

    def draw(self, screen):
        """Draw the surfaces on the screen"""
        for surface, pos, _ in self.surfaces:
            screen.blit(surface, pos)

@dataclass(slots=True)
class Game:
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption("Freefall")
    clock = pygame.time.Clock()
    chicken: Chicken = field(default_factory=Chicken)
    obstacles: Obstacles = field(default_factory=Obstacles)
    background: Background = field(default_factory=Background)

    def __init__(self):
        self.chicken = Chicken()
        self.obstacles = Obstacles()
        self.background = Background()

    def run(self):
        while 1:
            self.clock.tick(FPS)
            deltaTime: float = self.clock.get_time() / 1000
            self.events()
            self.update(deltaTime)
            self.draw()

    def update(self, deltaTime: float):
        self.chicken.update(deltaTime)
        self.obstacles.update(deltaTime)
        self.background.update(deltaTime)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    self.chicken.jump()
                if event.key == pygame.K_LEFT:
                    self.chicken.move_left(True)
                if event.key == pygame.K_RIGHT:
                    self.chicken.move_right(True)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.chicken.move_left(False)
                if event.key == pygame.K_RIGHT:
                    self.chicken.move_right(False)

 
    def draw(self):
        self.screen.fill(BackgroundColor)

        self.background.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.chicken.draw(self.screen)

        pygame.display.flip()

if __name__ == "__main__":
    Game().run()
