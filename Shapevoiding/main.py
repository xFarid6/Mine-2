import colorsys
import os
from typing import Any
import pygame
from pygame.locals import *
from constants import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Width, Height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.dt: float = 0.0
        self.game_elements: list[Any] = []
        self.player = Player()
        self.game_elements.append(self.player)

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60)
            self.events()
            self.update(self.dt)
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    pygame.quit()
                    quit()

    def update(self, dt: float):
        for element in self.game_elements:
            element.update(dt)

    def draw(self):
        self.screen.fill(BackgroundColor)
        for element in self.game_elements:
            element.draw(self.screen)
        pygame.display.flip()


class Player:
    def __init__(self):
        self.position = pygame.Vector2(Width/2, Height/2)
        self.maup_idle: list[pygame.surface.Surface] = [pygame.image.load("idle/{image}".format(image=i)) for i in os.listdir("idle") if i.endswith(".png")]
        self.player_rect: pygame.rect.Rect = self.maup_idle[0].get_rect(center=self.position)
        self.player_current: pygame.surface.Surface = self.maup_idle[0]
        self.player_index: float = 0.0
        self.left: bool = False
    
    def hsv2rgb(self, h: int | float, s: int, v: int) -> tuple[int, ...]:
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    def update(self, dt: float):
        self.color = (self.hsv2rgb((self.position.x+self.position.y)/1000 , 1, 1) )
        events = pygame.key.get_pressed()
        #left = False
        #right = False
        if events[K_w]:
            self.position.y -= 10
        if events[K_s]:
            self.position.y += 10
        if events[K_a]:
            self.position.x -= 10
            #left, right = not right, left
            self.left = True
        if events[K_d]:
            self.position.x += 10
            #right, left = not left, right
            self.left = False

        self.player_rect = self.player_current.get_rect(center=self.position)
        self.player_index += 0.1
        if self.player_index >= len(self.maup_idle):
            self.player_index = 0.0
        
        if self.left:
            self.player_current = pygame.transform.flip(self.maup_idle[int(self.player_index)], True, False)
        else:
            self.player_current = self.maup_idle[int(self.player_index)]

        '''if left:
            self.player_current = pygame.transform.flip(self.player_current, True, False)
            self.player_current = self.maup_idle[int(self.player_index)]
        if right:
            self.player_current = self.maup_idle[int(self.player_index)]'''


    def draw(self, surface):
        surface.blit(
            pygame.transform.scale(self.player_current, (self.player_rect.width * 2, self.player_rect.height * 2)), 
            self.position
            )


if __name__ == '__main__':
    Game().run()