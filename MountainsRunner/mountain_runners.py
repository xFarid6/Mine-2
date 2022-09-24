from __future__ import annotations 
from dataclasses import dataclass, field
from typing import Any, Sequence
import os

import pygame

from constants import BackgroundColor, Width, Height, FPS, color_codes
from player import Player


@dataclass(slots=True)
class Game:
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption("Mountain Runners")
    clock = pygame.time.Clock()

    bg: Background
    player: Player
    game_layers: dict[str, Any] = field(init=False, default_factory=dict)
    keys: Sequence[bool] = field(init=False, default_factory=list)

    def __init__(self):
        self.bg: Background = Background()
        self.player: Player = Player()

        self.game_layers = {
            "background": self.bg,
            "player": self.player,
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        self.keys = pygame.key.get_pressed()

    def draw(self):
        self.screen.fill(BackgroundColor)
        for name, layer in self.game_layers.items():
            layer.draw(self.screen)

        pygame.display.flip()


class Background:
    def __init__(self):
        self.images: dict[str, list] = {}
        self.render_order: dict[str, float] = {  # type: ignore
                    "bg.png": 0, 
                    "montain-far.png": 1, 
                    "mountains.png": 2, 
                    "trees.png": 4, 
                    "foreground-trees.png": 8
                    }

        # self.render_order: dict[float, str] = {k: v for v, k in sorted(self.render_order.items())}

        # load images
        for img in os.listdir("layers"):
            name = img[18:]
            loaded = pygame.image.load(f"layers/{img}").convert_alpha()
            loaded = pygame.transform.scale(loaded, (Width, Height))
            self.images[name] = [loaded, loaded.get_rect()]
            # {"bg.png": [surf, rect]}"}

    def update(self, deltaTime: float):
        # parallax effect
        for name, group in self.images.items():
            img, rect = group
            rect.x -= self.render_order.get(name)
            if rect.x <= -Width:
                rect.x = 0

    def draw(self, screen: pygame.Surface):
        for key, value in self.render_order.items():
            img, rect = self.images[key]
            screen.blit(img, rect)
            screen.blit(img, (rect.x + Width, rect.y))
            

if __name__ == "__main__":
    Game().run()