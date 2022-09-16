import math
import pygame
import sys
import random

"""
FLAGS
"""

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Particle Glow')
screen = pygame.display.set_mode((700, 600), 0, 32)

def circle_surf(radius: int, color: tuple[int, int, int]) -> pygame.surface.Surface:
    """
    It creates a circle surface.
    
    Args:
      radius (int): The radius of the circle.
      color (tuple[int, int, int]): The color of the circle.
    
    Returns:
      pygame.surface.Surface: The circle surface.
    """
    surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0,0,0))
    return surf

particles = []
font = pygame.font.SysFont('Arial', 48)

pos = [350, 300]

while True:

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (50, 20, 120), (100, 100, 200, 80))

    mx, my = pos # pygame.mouse.get_pos()
    particles.append([[mx, my], [random.randint(0, 20) / 10 - 1, -5], random.randint(6, 11)])

    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        particle[1][1] += 0.15
        pygame.draw.circle(screen, (255, 255, 255), (int(particle[0][0]), int(particle[0][1])), int(particle[2]))

        radius = particle[2] * 2
        screen.blit(circle_surf(radius, (20, 20, 70)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=pygame.BLEND_RGBA_ADD)

        if particle[2] <= 0:
            particles.remove(particle)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # make the pos point move in a circle around the center of the screen
    pos[0] = 350 + 200 * math.sin(pygame.time.get_ticks() / 1000)
    pos[1] = 300 + 200 * math.cos(pygame.time.get_ticks() / 1000)


    text = font.render('Particles: ' + str(len(particles)), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.topleft = (10, 10)
    screen.blit(text, textRect)

    pygame.display.update()
    mainClock.tick(30)

