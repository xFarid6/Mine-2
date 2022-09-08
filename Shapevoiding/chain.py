import pygame
from verlet import VerletObject, Solver, Link
import time
import random

Width = 1000
Height = 800

size: tuple[int, int] = (Width, Height)
pygame.init()
pygame.font.init()
screen: pygame.surface.Surface = pygame.display.set_mode(size)
pygame.display.set_caption("Verlet Simulation")
clock: pygame.time.Clock = pygame.time.Clock()

run: bool = True
clicked: bool = False

verletObjects = [VerletObject(500, 80), VerletObject(500, 120)]
solver = Solver(verletObjects)
link = Link(solver.verlet_objects[0], solver.verlet_objects[1], 40)

now = time.time()
last_time = now

def draw_text(text, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont("Arial", 20)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

while run:
    clock.tick(60)
    deltaTime = now - last_time
    last_time = now
    now = time.time()

    screen.fill((30, 30, 30))

    draw_text(f'Objects: {len(verletObjects)}', 10, 10)
    draw_text(f'FPS: {int(clock.get_fps())}', 10, 30)

    solver.update(deltaTime)
    #link.apply()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    pygame.display.flip()
    
pygame.quit()