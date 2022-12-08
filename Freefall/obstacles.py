import pygame
from queue import Queue
import random
from constants import Width, Height, color_codes


class Obstacles:
    def __init__(self):
        self.obstacles = list()
        self.width = 200
        self.height = 40
        self.obstacle = pygame.Rect(Width // 2 - self.width // 2, Height + self.height, self.width, self.height)
        self.obstacle_speed: int = 2

        self.time_start = pygame.time.get_ticks()
        self.time_span: int = 750 # 1000
        self.generated: int = 0

        self.colors = iter(list(color_codes.values())[:10])

        self.obstacles.append(self.obstacle)

    def update(self, deltaTime: float, chicken):
        """Obstacles should be generated belowe the screen and deleted when they get above the screen"""

        # generate and add to queue every time_span seconds
        if pygame.time.get_ticks() - self.time_start > self.time_span:
            obstacle = self.obstacle.copy()
            obstacle.x = random.randint(0, Width - obstacle.width)
            obstacle.y = Height + self.obstacle.height
            self.obstacles.append(obstacle)
            self.time_start = pygame.time.get_ticks()
            
            self.generated += 1
            # self.time_span -= self.generated * 10

        speed_up = 0 if not chicken.on_air else chicken.vel_y

        # update obstacle position
        for obstacle in self.obstacles:
            obstacle.y -= self.obstacle_speed + speed_up

        # delete obstacle when it gets above the screen
        for obstacle in self.obstacles:
            if obstacle.y < 0 - self.obstacle.height:
                self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            try:
                color = next(self.colors)
            except StopIteration:
                self.colors = iter(color_codes.values())
                color = next(self.colors)

            pygame.draw.rect(screen, (100, 100, 100), obstacle)
