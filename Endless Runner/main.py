# using event queue pattern

# care for states and Enums

# observer pattern for achievments

# using command pattern for player movement


from typing import NoReturn

from player import Commands, Player
from world import World

from pygame.locals import *
import pygame


class EndlessRunner: 
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.width = 400
        self.height = 300
        self.small_screen = pygame.Surface((self.width, self.height))
        self.big_screen = pygame.display.set_mode((800,600))

        self.clock = pygame.time.Clock()
        self.fps: int = 30
        self.getTicksLastFrame: int = 0

        self.game_objects: list = []

        self.pause: bool = False

        self.world: World = World(self)

        self.player: Player = Player(self)


    def get_dt(self) -> int: 
        time: int = pygame.time.get_ticks()
        # deltaTime in seconds.
        deltaTime: float = (time - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = time

        return int(deltaTime)


    def update(self, dt: int) -> None: 
        for elem in self.game_objects:
            elem.update(dt)


    def render(self, small_screen) -> None:
        for elem in self.game_objects:
            elem.render(small_screen)
        
        self.big_screen.blit(
            pygame.transform.scale(small_screen, self.big_screen.get_size()),
            (0, 0)
        )

        pygame.display.flip()


    def run(self) -> NoReturn:
        while True:
            dt = self.get_dt()
            self.update(dt)
            self.render(self.small_screen)
            self.clock.tick(self.fps)


if __name__ == '__main__':
    game = EndlessRunner()
    game.run()