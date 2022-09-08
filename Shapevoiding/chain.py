import pygame
from verlet_with_links import VerletObject, Solver, Link
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

now = time.time()
last_time = now

def draw_text(text, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont("Arial", 20)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

x, y = 50, 50
t = 20
vertices = []
for j in range(10):
    for i in range(10):
        vertices.append( VerletObject(x+i*t, y+j*t, 5) )

joints: list = []

# horizontal connection
for i in range(len(vertices)-1):
    if i % 10 != 10 -1:
        joints.append([i, i+1])

# Vertical connection
for i in range(len(vertices) - 10):
    joints.append( [i, i+10] )

#first diagonal connection
for i in range(len(vertices) - 10-1):
    if i %10 != 10-1:
        joints.append( [i, i + 10 + 1] )
# second diagonal connection
for i in range(len(vertices) - 10):
    if i % 10 != 0:
        joints.append( [i, i+10-1] )

static = [vertices[0], vertices[10//2], vertices[10-1]]

links = []
for i in range(len(joints)):
    links.append( Link(vertices[joints[i][0]], vertices[joints[i][1]], 30) )
solver = Solver(vertices, links)

c1v = VerletObject(0, 0)
corner1 = Link(c1v, vertices[0], 30)
c2v = VerletObject(0, Height)
corner2 = Link(c2v, vertices[10-1], 30)
c3v = VerletObject(Width, 0)
corner3 = Link(c3v, vertices[10*(10-1)], 30)
c4v = VerletObject(Width, Height)
corner4 = Link(c4v, vertices[-1], 30)

while run:
    clock.tick(60)
    deltaTime = now - last_time
    last_time = now
    now = time.time()

    screen.fill((30, 30, 30))

    solver.update(deltaTime)
    c1v = VerletObject(0, 0)
    c1v.draw(screen)
    corner1.draw()
    corner1.apply()
    c2v = VerletObject(0, Height)
    c2v.draw(screen)
    corner2.draw()
    corner2.apply()
    c3v = VerletObject(Width, 0)
    c3v.draw(screen)
    corner3.draw()
    corner3.apply()
    c4v = VerletObject(Width, Height)
    c4v.draw(screen)
    corner4.draw()
    corner4.apply()

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