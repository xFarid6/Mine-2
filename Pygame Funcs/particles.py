import os
import random
from typing import Sequence

import pygame

global e_colorkey
e_colorkey: tuple[int, int, int] = (0, 0, 0)
global particle_images
particle_images: dict[str, list[pygame.surface.Surface]] = {}

def circle_surf(size: int, color: tuple[int, int, int] | pygame.Color) -> pygame.surface.Surface:
    surf: pygame.surface.Surface = pygame.Surface((size * 2 + 2, size * 2 + 2))
    pygame.draw.circle(surf, color, (size + 1, size + 1), size)
    return surf

def blit_center(target_surf: pygame.surface.Surface, surf: pygame.surface.Surface, loc: Sequence[int]) -> None:
    target_surf.blit(surf, (loc[0] - surf.get_width() // 2, loc[1] - surf.get_height() // 2))

def blit_center_add(target_surf: pygame.surface.Surface, surf: pygame.surface.Surface, loc: Sequence[int]) -> None:
    target_surf.blit(surf, (loc[0] - surf.get_width() // 2, loc[1] - surf.get_height() // 2), special_flags=pygame.BLEND_RGBA_ADD)

def particle_file_sort(l: list[str]) -> list[str]:
    """
    It takes a list of strings, each of which is a file name, and returns a list of strings, each of
    which is a file name, but sorted
    
    Args:
      l (list): list = list of files in the directory
    
    Returns:
      A list of strings.
    """
    l2: list[int] = []
    for obj in l:
        l2.append(int(obj[:-4]))
    l2.sort()
    l3: list = []
    for obj in l2:
        l3.append(str(obj) + '.png')
    return l3

def load_particle_images(path: str) -> None:
    """
    It loads all the images in a folder into a list, then adds that list to a dictionary.
    
    Args:
      path (str): str = The path to the folder containing the particle images.
    """
    global particle_images, e_colorkey

    file_list: list[str] = os.listdir(path)
    for folder in file_list:
        #try:
        img_list: list[str] = os.listdir(path + '/' + folder)
        img_list = particle_file_sort(img_list)
        images: list[pygame.surface.Surface] = []
        for img in img_list:
            images.append(pygame.image.load(path + '/' + folder + '/' + img).convert())
        for img in images:
            img.set_colorkey(e_colorkey)
        particle_images[folder] = images.copy()
        #except:
        #    pass

class Particle(object):

    def __init__(self, x: int, y: int, particle_type: str, motion, decay_rate: float, start_frame: int, custom_color: tuple[int, int, int] | None=None, physics: bool=False):
        self.x = x
        self.y = y
        self.type = particle_type
        self.motion = motion
        self.decay_rate = decay_rate
        self.color = custom_color
        self.frame: float = start_frame
        self.physics = physics
        self.orig_motion = self.motion
        self.temp_motion: list[int] = [0, 0]
        self.time_left: float = len(particle_images[self.type]) + 1 - self.frame
        self.render: bool = True
        self.random_constant: float = random.randint(20, 30) / 30

    def draw(self, surface: pygame.surface.Surface, scroll: Sequence[int]) -> None:
        """
        It draws a particle to the screen
        
        Args:
          surface (pygame.surface.Surface): The surface to draw the particle on.
          scroll (Sequence[int]): The scroll of the screen.
        """
        global particle_images

        if self.render:
            #if self.frame > len(particle_images[self.type]):
            #    self.frame = len(particle_images[self.type])
            if self.color == None:
                blit_center(
                    surface, 
                    particle_images[self.type][int(self.frame)], 
                    (self.x-scroll[0], self.y-scroll[1])
                )
            else:
                blit_center(
                    surface, 
                    swap_color(particle_images[self.type][int(self.frame)], (255,255,255), self.color), 
                    (self.x-scroll[0], self.y-scroll[1])
                )

    def update(self, dt: float) -> bool:
        """
        It updates the particle's position, frame, and time left
        
        Args:
          dt (float): float = time since last update
        
        Returns:
          The return value is a boolean value representing if the particle's stil alive.
        """
        self.frame += self.decay_rate * dt
        self.time_left: float = len(particle_images[self.type]) + 1 - self.frame
        running: bool = True
        self.render = True
        if self.frame >= len(particle_images[self.type]):
            self.render = False
            if self.frame >= len(particle_images[self.type]) + 1:
                running = False
            running = False
        if not self.physics:
            self.x += (self.temp_motion[0] + self.motion[0]) * dt
            self.y += (self.temp_motion[1] + self.motion[1]) * dt
            if self.type == 'p2':
                self.motion[1] += dt * 140
        self.temp_motion = [0, 0]

        return running


# other useful functions

def swap_color(img: pygame.surface.Surface, old_c: tuple[int, int, int], new_c: tuple[int, int, int]) -> pygame.surface.Surface:
    """
    It takes an image, sets the colorkey to the old color, copies the image, fills the copy with the new
    color, blits the old image onto the copy, and then sets the colorkey back to the original color
    
    Args:
      img (pygame.surface.Surface): The image to be swapped
      old_c (tuple[int, int, int]): The color you want to change
      new_c (tuple[int, int, int]): The color you want to change the old_c to.
    
    Returns:
      A surface with the color changed.
    """
    global e_colorkey

    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img,(0,0))
    surf.set_colorkey(e_colorkey)

    return surf
