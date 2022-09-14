from dataclasses import dataclass, field
from constants import Width, Height, draw_text, color_codes
from os import listdir
from main import Game
import numpy as np 
import pygame


@dataclass(slots=True)
class Player:
    game: Game 
    idle: dict[int, pygame.surface.Surface] = field(default_factory=dict)
    run: dict = field(default_factory=dict)
    
    player_rect: pygame.rect.Rect = pygame.Rect(Width/2, Height/2, 0, 0)
    player_state: str = 'idle'
    player_frame: float = 0
    player_image: pygame.surface.Surface = pygame.Surface((0, 0))
    velocity: np.ndarray = np.array([0, 0], dtype=np.int8)
    max_velocity: int = 7

    lives: int = 3
    font: pygame.font.Font = pygame.font.SysFont('comicsans', 20)
    left: bool = False

    def __post_init__(self):
        for x, y in enumerate(listdir(r"C:\Cose Nuove\Code\Mine 2\Shapevoiding\idle")):
            if y.endswith('.png'):
                img = pygame.image.load("C:\\Cose Nuove\\Code\\Mine 2\\Shapevoiding\\idle\\" + y).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.idle[x] = img
        
        for x, y in enumerate(listdir(r"C:\Cose Nuove\Code\Mine 2\Shapevoiding\run")):
            if y.endswith('.png'):
                img = pygame.image.load("C:\\Cose Nuove\\Code\\Mine 2\\Shapevoiding\\run\\" + y).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.run[x] = img

        self.player_rect = self.idle[0].get_rect(center=(Width/2, Height/2))

    def move(self, keys: dict[int, bool]):
        if keys.get(pygame.K_a):
            self.velocity[0] -= 1
        if keys.get(pygame.K_d):
            self.velocity[0] += 1
        if keys.get(pygame.K_w):
            self.velocity[1] -= 1
        if keys.get(pygame.K_s):
            self.velocity[1] += 1

        # if np.allclose(self.velocity, np.array([0, 0])):
        #   self.velocity = np.array([0, 0], dtype=np.int8)

        if not any(keys.values()):
            self.velocity = np.array([0, 0], dtype=np.int8)

        if self.velocity[0] > self.max_velocity:
            self.velocity[0] = self.max_velocity
        elif self.velocity[0] < -self.max_velocity:
            self.velocity[0] = -self.max_velocity
        if self.velocity[1] > self.max_velocity:
            self.velocity[1] = self.max_velocity
        elif self.velocity[1] < -self.max_velocity:
            self.velocity[1] = -self.max_velocity

        # self.player_rect.move_ip(*self.velocity)
        self.player_rect.x += self.velocity[0]
        self.player_rect.y += self.velocity[1]

    def constraints(self):
        if self.player_rect.left < 0:
            self.player_rect.left = 0
            self.velocity[0] = 0
        elif self.player_rect.right > Width:
            self.player_rect.right = Width
            self.velocity[0] = 0
        elif self.player_rect.top < 0:
            self.player_rect.top = 0
            self.velocity[1] = 0
        elif self.player_rect.bottom > Height:
            self.player_rect.bottom = Height
            self.velocity[1] = 0

    def update_player_image(self, dt: float):
        self.player_frame += 10 * dt
        # print(self.player_frame)

        if np.allclose(self.velocity, np.array([0, 0])):
            self.player_state = 'idle'
            self.player_image = self.idle.get(int(self.player_frame) % len(self.idle), self.idle[0])
        else:
            self.player_state = 'run'
            self.player_image = self.run.get(int(self.player_frame) % len(self.run), self.run[0])

        if self.velocity[0] < 0:
            self.left = True
        elif self.velocity[0] > 0:
            self.left = False

        if self.left:
            self.player_image = pygame.transform.flip(self.player_image, True, False)

    def update(self, dt: float):
        
        self.move(self.game.pressed_keys)
        self.constraints()
        self.update_player_image(dt)

    def draw(self):
        draw_text(f'Lives: {self.lives}', self.font, color_codes['medium violet red'], self.game.screen, 50, 20)

        self.game.screen.blit(
            self.player_image, 
            self.player_rect
            )

if __name__ == '__main__':
    Game().run()
