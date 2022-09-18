import random
import pygame
from dataclasses import dataclass, field
from constants import BackgroundColor, Width, Height, FPS, color_codes

@dataclass(slots=True)
class Game:
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption("Freefall")
    clock = pygame.time.Clock()

    def __init__(self):
        ...

    def run(self):
        while 1:
            self.clock.tick(FPS)
            deltaTime: float = self.clock.get_time() / 1000
            self.events()
            self.update(deltaTime)
            self.draw()

    def update(self, deltaTime: float):
        ...

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def draw(self):
        self.screen.fill(BackgroundColor)

        pygame.display.flip()

if __name__ == "__main__":
    Game().run()
