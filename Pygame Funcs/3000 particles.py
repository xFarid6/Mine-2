import random
import sys
import pygame
from pygame.locals import *

"""
SPECIAL HASHING
"""

pygame.init()
screen = pygame.display.set_mode((700, 600), 0, 32)
pygame.display.set_caption('3000 particles')
mainClock = pygame.time.Clock()

tile_size = 20

particles = []

tile_map = {}
for i in range(10):
    tile_map[str(i + 4) + ';14'] = [i + 4, 14, (255, 0, 0)]

tile_map['15;10'] = [15, 10, (0, 255, 0)]
tile_map['15;11'] = [15, 11, (0, 255, 0)]
tile_map['15;12'] = [15, 12, (0, 255, 0)]
tile_map['15;13'] = [15, 13, (0, 255, 0)]

tile_map['11;11'] = [11, 11, (0, 0, 255)]
tile_map['11;12'] = [11, 12, (0, 0, 255)]

clicking = False

font = pygame.font.SysFont('Arial', 30)

while True:
    screen.fill((0, 0, 0))
    mx, my = pygame.mouse.get_pos()

    if clicking:
        for i in range(60):
            particles.append([[mx, my], [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5], random.randint(4, 6)])

    for particle in particles:
        particle[0][0] += particle[1][0]
        loc_str = str(int(particle[0][0] / tile_size)) + ';' + str(int(particle[0][1] / tile_size))
        if loc_str in tile_map:
            particle[1][0] *= -0.7
            particle[1][1] *= -0.95
            particle[0][0] += particle[1][0] * 2
        particle[0][1] += particle[1][1]
        loc_str = str(int(particle[0][0] / tile_size)) + ';' + str(int(particle[0][1] / tile_size))
        if loc_str in tile_map:
            particle[1][1] *= -0.7
            particle[1][0] = particle[1][0] * 0.95
            particle[0][1] += particle[1][1] * 2
        particle[2] -= 0.035
        particle[1][1] += 0.15
        pygame.draw.circle(screen, (255, 255, 255), (int(particle[0][0]), int(particle[0][1])), int(particle[2]))

        if particle[2] <= 0:
            particles.remove(particle)

    for tile in tile_map:
        pygame.draw.rect(
            screen, 
            tile_map[tile][2], 
            (tile_map[tile][0] * tile_size, tile_map[tile][1] * tile_size, tile_size, tile_size))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            clicking = True
        if event.type == MOUSEBUTTONUP:
            clicking = False

    fps = font.render("FPS: " + str(int(mainClock.get_fps())), True, (255, 255, 255))
    screen.blit(fps, (0, 0))
    particles_number = font.render("Particles: " + str(len(particles)), True, (255, 255, 255))
    screen.blit(particles_number, (0, 30))

    pygame.display.update()
    mainClock.tick(60)
