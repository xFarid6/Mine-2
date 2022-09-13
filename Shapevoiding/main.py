from constants import Width, Height, BackgroundColor, FPS, draw_text, color_codes
from dataclasses import dataclass, field
from typing import Any
import numpy as np 
import pygame

@dataclass(slots=True)
class Game:
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    flags: int = pygame.DOUBLEBUF
    screen = pygame.display.set_mode(size=(Width, Height), flags=flags, depth = 16, vsync=1)
    clock = pygame.time.Clock()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
    game_objects: dict[str, Any] = field(default_factory=dict)
    font: pygame.font.Font = pygame.font.SysFont('Arial', 15)
    pressed_keys: dict[int, bool] = field(default_factory=dict)

    def __post_init__(self):
        from player import Player
        self.game_objects['player'] = Player(self)

        from shapes import Shapes
        self.game_objects['shapes'] = Shapes(self)

    def run(self):
        while 1:
            dt: float = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update(dt)
            self.draw()

    def events(self):
        keys = pygame.key.get_pressed()
        self.pressed_keys = {key: keys[key] for key in range(len(keys)) if keys[key]}
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update(self, dt: float):
        for game_object in self.game_objects.values():
            game_object.update(dt)

    def draw(self):
        self.screen.fill(BackgroundColor)
        draw_text(f'FPS: {self.clock.get_fps():.3f}', self.font, color_codes.get('white smoke'), self.screen, 50, 50)

        for game_object in self.game_objects.values():
            game_object.draw()

        pygame.display.flip()

if __name__ == '__main__':
    Game().run()