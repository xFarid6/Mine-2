from constants import Width, Height, color_codes
from dataclasses import dataclass, field
from random import choice, randint
from typing import Any
from main import Game
import numpy as np 
import pygame


class Square:
    def __init__(self):
        self.x = randint(0, Width)
        self.y = randint(0, Height)
        self.width = randint(10, 50)
        self.height = randint(10, 50)
        self.color = choice(list(color_codes.values()))
        self.vel = np.array([randint(-10, 10), randint(-10, 10)])
        self.pos = np.array([self.x, self.y])

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shape = self.rect.copy()

        if self.vel[0] == 0:
            self.vel[0] = 1
        if self.vel[1] == 0:
            self.vel[1] = 1

    def update_position(self):
        self.pos += self.vel
        self.x, self.y = self.pos

    def constraints(self):
        if self.x < 0 or self.x > Width - self.width:
            self.vel[0] *= -1
        if self.y < 0 or self.y > Height - self.height:
            self.vel[1] *= -1

    def move(self, dt: float):
        self.update_position()
        self.constraints()

    def draw(self, win):
        self.shape = pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


class Rectangle:
    def __init__(self):
        self.x = randint(0, Width)
        self.y = randint(0, Height)
        self.width = randint(10, 50)
        self.height = randint(10, 50)
        self.color = choice(list(color_codes.values()))
        self.velocity = np.array([randint(-10, 10), randint(-10, 10)])
        self.pos = np.array([self.x, self.y])

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shape = self.rect.copy()

        if self.velocity[0] == 0:
            self.velocity[0] = 1
        if self.velocity[1] == 0:
            self.velocity[1] = 1

    def update_position(self):
        self.pos += self.velocity
        self.x, self.y = self.pos

    def constraints(self):
        if self.x < 0:
            self.x = 0
            self.velocity[0] *= -1
        if self.x + self.width > Width:
            self.x = Width - self.width
            self.velocity[0] *= -1
        if self.y < 0:
            self.y = 0
            self.velocity[1] *= -1
        if self.y + self.height > Height:
            self.y = Height - self.height
            self.velocity[1] *= -1

    def move(self, dt: float):
        self.update_position()
        self.constraints()

    def draw(self, win):
        self.shape = pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


class Triangle:
    def __init__(self):
        self.x = randint(0, Width)
        self.y = randint(0, Height)
        self.width = randint(10, 50)
        self.height = randint(10, 50)
        self.color = choice(list(color_codes.values()))
        self.pos = np.array([self.x, self.y])
        self.vel = np.array([randint(-5, 5), randint(-5, 5)], dtype=np.int8)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shape = self.rect.copy()

        if self.vel[0] == 0:
            self.vel[0] = 1
        if self.vel[1] == 0:
            self.vel[1] = 1

    def update_pos(self):
        self.pos += self.vel
        self.x, self.y = self.pos

    def constraints(self):
        if self.x < 0:
            self.x = 0
            self.vel[0] *= -1
        elif self.x + self.width > Width:
            self.x = Width - self.width
            self.vel[0] *= -1
        if self.y < 0:
            self.y = 0
            self.vel[1] *= -1
        elif self.y + self.height > Height:
            self.y = Height - self.height
            self.vel[1] *= -1

    def move(self, dt: float):
        self.update_pos()
        self.constraints()
    
    def draw(self, win):
        self.shape = pygame.draw.polygon(win, self.color, ((self.x, self.y), (self.x + self.width, self.y), (self.x + self.width / 2, self.y + self.height)))


class Circle:
    def __init__(self):
        self.x = randint(15, Width-15)
        self.y = randint(15, Height-15)
        self.radius = 15
        self.pos: np.ndarray = np.array([self.x, self.y])
        self.color = choice(list(color_codes.values()))
        self.velocity = np.array([randint(-5, 5), randint(-5, 5)], dtype=np.int8)

        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.shape = self.rect.copy()

        if self.velocity[0] == 0:
            self.velocity[0] = 1
        if self.velocity[1] == 0:
            self.velocity[1] = 1

    def update_pos(self, dt: float):
        self.pos += self.velocity * int(dt + 1)
        self.x, self.y = self.pos

    def constrain(self):
        if self.x < 0 + self.radius:
            self.velocity[0] *= -1
        if self.x > Width - self.radius:
            self.velocity[0] *= -1
        if self.y < 0 + self.radius:
            self.velocity[1] *= -1
        if self.y > Height - self.radius:
            self.velocity[1] *= -1

    def move(self, dt: float):
        self.update_pos(dt)
        self.constrain()

    def draw(self, win):
        self.shape = pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


@dataclass(slots=True)
class Shapes:
    game: Game
    spawn: bool = True

    created_shapes: dict[str, Any] = field(default_factory=dict)
    shape_associasions: dict[str, Any] = field(default_factory=dict)
    start_time: int = pygame.time.get_ticks()   
    now_time: int = pygame.time.get_ticks()       

    def __post_init__(self):
        self.shape_associasions.update({'triangle': Triangle, 
                                        'circle': Circle, 
                                        'square': Square, 
                                        'rectangle': Rectangle}
                                        )
        self.created_shapes.update({'circle': Circle()})

    def update(self, dt: float):
        self.now_time = pygame.time.get_ticks()
        if self.now_time - self.start_time >= 2000:
            self.spawn = True
            self.start_time = self.now_time
        
        # add shape to created_shapes
        if self.spawn:
            shape = choice(list(self.shape_associasions.keys()))
            # print(shape)
            new_shape_key = shape + str(pygame.time.get_ticks())
            self.created_shapes.update({new_shape_key: self.shape_associasions.get(shape, Circle)()})
            # pprint(self.created_shapes)
            self.spawn = False

        for shape in self.created_shapes.values():
            shape.move(dt)

    def draw(self):
        for shape in self.created_shapes.values():
            shape.draw(self.game.screen)
            # pygame.draw.rect(self.game.screen, (255, 255, 255), shape.shape, 1)


if __name__ == '__main__':
    Game().run()