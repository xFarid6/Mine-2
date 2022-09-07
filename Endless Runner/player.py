import os
from typing import Callable, Dict, List
from pygame.locals import *
from user import Settings
import pygame


class Player:
    def __init__(self, base_game):
        # base game
        self.base_game = base_game
        self.base_game.game_objects.append(self)

        # fox related
        self.fox: pygame.surface.Surface = pygame.image.load("Endless Runner/Fox Sprite Sheet.png")
        self.foxes: Dict[str, List[pygame.Surface]] = self.load_anims(
            32, 
            anim_names=['wiggle_tail', 'look_around', 'walking', 'jumping', 'idk', 'sleeping', 'shaking'],
            frames=[5, 14, 8, 11, 5, 6, 7])
        self.fox_rect: pygame.Rect = pygame.Rect(0, 0, 64, 64)
        self.fox_index: float = 0
        self.current_animation: str = 'look_around'

        # orb
            # orb image
        self.orb: list[pygame.surface.Surface] = [pygame.image.load("Endless Runner/orb_idle/"+file) for file in os.listdir("Endless Runner/orb_idle") if file.endswith('.png')]
        self.orb_index: float = 0
        self.orb_current_animation: pygame.surface.Surface = self.orb[0]
        self.orb_rect: pygame.rect.Rect = self.orb_current_animation.get_rect(topleft=(10, 100))
        for img in self.orb:
            img.set_colorkey((0, 0, 0))

            # orb gravity
        self.orb_velocity: float = 1
        self.gravity: float = .5

        # colors
        self.active_color: tuple[int, int, int] = Settings.night_color

        # trying command pattern
        self.command_dispatcher: Commands = Commands()
        self.player_actions: Dict[str, Callable] = {  # type: ignore
            'space': self.jumping,
            'down': None, 
            'up': None,
            'left': None,
            'right': None
        }

    
    def is_day(self) -> bool:
        """if the orb is above half screen"""
        return self.orb_rect.y < self.base_game.height / 2

    def is_night(self) -> bool:
        """if the orb is below half screen"""
        return self.orb_rect.y > self.base_game.height / 2
    
    def orb_platform_collisions(self):
        """
        If the orb collides with a platform, set the orb's velocity to zero. 
        Otherwise, increase the orb's velocity by 1%
        """
        for platform in self.base_game.world.platforms:
            if self.orb_rect.colliderect(platform):
                self.orb_velocity = 0
        else:
            self.orb_velocity *= 1.01 # this increment must be smaller than gravity

    def orb_line_collision(self):
        clipped_line = self.orb_rect.clipline(self.base_game.world.line_points)

        if clipped_line:
            # If clipped_line is not an empty tuple then the line
            # collides/overlaps with the rect. The returned value contains
            # the endpoints of the clipped line.
            start, end = clipped_line
            x1, y1 = start
            x2, y2 = end
            self.orb_velocity = 0

    def apply_gravity(self):
        self.orb_velocity += self.gravity

        # day
        if self.is_day():
            self.gravity = 1 * abs(self.gravity)
        # night
        if self.is_night():
            self.gravity = - 1 * abs(self.gravity)

        self.orb_rect.y += int(self.orb_velocity)

    def handle_movement(self, actions: dict[str, bool]) -> None:
        for action, did_it in actions.items():
            if did_it:
                self.player_actions[action](actions)

    def jumping(self, actions) -> None:
        self.orb_velocity = 0
        if self.is_day():
            self.orb_rect.y -= 4
            actions['space'] = False
        if self.is_night():
            self.orb_rect.y += 4
            actions['space'] = False
    
    def update(self, dt):
        # fox part
        self.fox_index += 0.2
        if self.fox_index >= len(self.foxes[self.current_animation]):
            self.fox_index = 0
        self.fox_rect.bottom = self.base_game.height

        # orb
        self.orb_current_animation = self.orb[int(self.orb_index)]
        self.orb_index += 0.3
        if self.orb_index >= len(self.orb):
            self.orb_index = 0

        # commands
        actions: dict[str, bool] = self.command_dispatcher.handle_events()

        # handle collisions
        # self.orb_platform_collisions()
        self.handle_movement(actions)
        self.apply_gravity()
        self.orb_line_collision()
        
    def render(self, screen):
        # fox
        screen.blit(
            pygame.transform.scale(
                self.foxes[self.current_animation][int(self.fox_index)], 
                (self.fox_rect.width, self.fox_rect.height),
                ),
            self.fox_rect
            )

        # orb
        screen.blit(
            # pygame.transform.scale2x(self.orb_current_animation),
            self.orb_current_animation,
            self.orb_rect
            )


    def image_at(self, rectangle: pygame.Rect, colorkey: int | None= None) -> pygame.surface.Surface:  # type: ignore
        """
        It takes a rectangle (x, y, width, height) and returns an image of that rectangle
        
        :param rectangle: The rectangle that defines the area of the sprite sheet to be cropped
        :param colorkey: If not None, this color will be transparent. If -1, the top left pixel will be
        transparent
        :return: The image at the given rectangle.
        """
        rect: pygame.Rect = pygame.Rect(rectangle)
        image: pygame.surface.Surface = pygame.Surface(rect.size).convert()
        image.blit(self.fox, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey: tuple[int, int, int, int] = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image


    def load_anims(self, size: int, anim_names: List[str], frames: List[int]) -> Dict[str, List[pygame.Surface]]:
        """
        It takes a spritesheet, a size, a list of animation names, and a list of frames per animation,
        and returns a dictionary of animation names mapped to lists of frames
        
        :param size: The size of each frame in the spritesheet
        :param anim_names: A list of strings that will be the names of the animations
        :param frames: The number of frames in the animation
        :return: A dictionary of lists of images.
        """
        # 1 quadetto sono 8 pixel, una volpe prende 4 quadretti in lunghezza
        # e facciamo anche 4 in altezza
        anims: dict = {}
        square: pygame.Rect = pygame.Rect(0, 0, size, size)
        for anim_name, anim_frame in zip(anim_names, frames):
            anims[anim_name]= []
            square.y = frames.index(anim_frame) * size
            for i in range(anim_frame):
                square.x = i * size
                anims[anim_name].append(self.image_at(square, -1))

        return anims


class Commands: 
    def __init__(self):
        self.actions: dict[str, bool] = {
            'space': False,
            'escape': False,
        }

    def handle_events(self):
        keys = pygame.key.get_pressed()

        if keys[K_q]: 
            pygame.quit()
            exit(0)
        if keys[K_ESCAPE]: self.actions['escape'] = True
        if keys[K_SPACE]: self.actions['space'] = True
        if keys[K_DOWN]: self.actions['down'] = True
        if keys[K_UP]: self.actions['up'] = True
        if keys[K_LEFT]: self.actions['left'] = True
        if keys[K_RIGHT]: self.actions['right'] = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        return self.actions
