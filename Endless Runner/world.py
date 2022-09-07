import random
import pygame
from user import Settings
from queue import Queue

class World: 
    def __init__(self, base_game):
        # base game
        self.base_game = base_game
        self.base_game.game_objects.append(self)

        # two parts of the screen
        self.day = pygame.Surface((self.base_game.width, self.base_game.height / 2))
        self.night = pygame.Surface((self.base_game.width, self.base_game.height / 2))
        self.day_rect: pygame.rect.Rect = self.day.get_rect()
        self.night_rect: pygame.rect.Rect = self.night.get_rect()

        # colors
        self.day.fill(Settings.day_color)
        self.night.fill(Settings.night_color)

        # platforms
        self.platforms: list[pygame.rect.Rect] = [
            pygame.Rect(
                0, 
                self.base_game.height / 2 - 5, 
                random.randint(100, 150),
                20
            ) for _ in range(5)
        ]
        self.assert_distances()
        self.p_speed: int = 5

        # line
        self.line_points = (
            (0, self.base_game.height / 2), 
            (self.base_game.width, self.base_game.height / 2)
            )

    def assert_distances(self):
        # assure distance is between 100 and 200
        for i, p in enumerate(self.platforms[:-1]):
            distance = self.platforms[i+1].topleft[0] - p.topright[0]
            if not 100 < distance < 150:
                self.platforms[i+1].topleft = (p.topright[0] + random.randint(100, 120), self.base_game.height / 2 - 5)

    def update(self, dt: int):
        for i, p in enumerate(self.platforms):
            p.x -= self.p_speed
            if p.topright[0] < 0: 
                self.platforms.append(self.platforms.pop(i)) # move to the back
                # p.width = random.randint(20, 50)
                self.assert_distances() # assert distance between all platforms



    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.day, (0, 0))
        screen.blit(self.night, self.day_rect.bottomleft)

        pygame.draw.line(screen, Settings.accent_color, self.line_points[0], self.line_points[1], 3)

        #for platform in self.platforms:
         #   pygame.draw.rect(screen, Settings.platform_color, platform)
        

class Spike:
    ...