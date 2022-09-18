from __future__ import annotations 
import os
from typing import Any
import pygame
from dataclasses import dataclass, field
from constants import BackgroundColor, Width, Height, FPS, color_codes

@dataclass(slots=True)
class Game:
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption("Mountain Runners")
    clock = pygame.time.Clock()

    bg: Background
    game_layers: dict[str, Any] = field(init=False, default_factory=dict)

    def __init__(self):
        self.bg: Background = Background()

        self.game_layers = {
            "background": self.bg,
        }

    def run(self):
        while 1:
            self.clock.tick(FPS)
            deltaTime: float = self.clock.get_time() / 1000
            self.events()
            self.update(deltaTime)
            self.draw()

    def update(self, deltaTime: float):
        for name, layer in self.game_layers.items():
            layer.update(deltaTime)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def draw(self):
        self.screen.fill(BackgroundColor)
        for name, layer in self.game_layers.items():
            layer.draw(self.screen)

        pygame.display.flip()

@dataclass(slots=True)
class Background:
    images: dict = field(default_factory=dict)
    render_order: tuple[str, ...] = ("bg.png", "montain-far.png", "mountains.png", "trees.png", "foreground-trees.png")

    def __post_init__(self):
        for idx, img in enumerate(os.listdir("layers")):
            name = img[18:]
            self.images[name] = pygame.image.load(f"layers/{img}").convert_alpha()
            self.images[name] = pygame.transform.scale(self.images[name], (Width, Height))

    def update(self, deltaTime: float):
        ...

    def draw(self, screen: pygame.Surface):
        for name in self.render_order:
            screen.blit(self.images[name], (0, 0))
            


if __name__ == "__main__":
    Game().run()