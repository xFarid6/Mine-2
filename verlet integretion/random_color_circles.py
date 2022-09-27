import colorsys
import os
import random
from typing import Any
import pygame
from pygame.locals import *
# from constants import *
Width = 800
Height = 600
BackgroundColor = (30, 30, 30)


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

        self.shapes = Shapes(self.player)
        self.game_elements.append(self.shapes)

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
        self.maup_idle: list[pygame.surface.Surface] = [
            pygame.image.load("idle/{image}".format(image=i)).convert_alpha() 
                for i in os.listdir("idle") if i.endswith(".png")
                ]
        self.player_rect: pygame.rect.Rect = self.maup_idle[0].get_rect(center=self.position)
        self.player_current: pygame.surface.Surface = self.maup_idle[0]
        self.player_index: float = 0.0
        self.left: bool = False
        self.heart: pygame.surface.Surface = pygame.image.load("lil_heart.png").convert_alpha()
        self.heart = pygame.transform.scale(self.heart, (self.heart.get_width()//5.5, self.heart.get_height()//5.5)).convert_alpha()
        self.heart.set_colorkey(color_codes.get("white"))
        self.max_lives: int = 3
        self.lives: int = self.max_lives
    
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
        for i in range(self.lives):
            surface.blit(
                self.heart, 
                (i*30, 10)
                )
        surface.blit(
            pygame.transform.scale(self.player_current, (self.player_rect.width * 2, self.player_rect.height * 2)), 
            self.position
            )


class Shapes:
    def __init__(self, player: Player):
        self.player = player
        self.n_shapes: int = 1
        self.radius: int = 10
        self.all_shapes = []

        self.font = pygame.font.SysFont("Arial", 30)
        

    def hsv2rgb(self, h: int | float, s: int, v: int) -> tuple[int, ...]:
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    def update(self, dt: float):
        time = pygame.time.get_ticks()
        self.n_shapes = time // 1000

    def draw(self, surface):
        time = pygame.time.get_ticks()
        time_text = self.font.render("Ticks: " + str(time), True, (255, 255, 255))
        n_shapes_text = self.font.render("Shapes: " + str(self.n_shapes), True, (255, 255, 255))
        surface.blit(time_text, (10, 40))
        surface.blit(n_shapes_text, (10, 70))

        for _ in range(self.n_shapes):
            x = random.randint(0 + self.radius, Width - self.radius)
            y = random.randint(0 + self.radius, Height - self.radius)
            self.all_shapes.append(pygame.Vector2(x, y))
        
        for x, y in self.all_shapes:
            pygame.draw.circle(
                surface, 
                self.hsv2rgb((x + y)/1000, 1, 1), 
                (x, y), 
                self.radius + 30
                )

if __name__ == '__main__':
    Game().run()