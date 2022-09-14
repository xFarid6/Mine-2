import pygame
pygame.init()
window = pygame.display.set_mode((250, 250))

background = pygame.Surface(window.get_size())
for x in range(5):
    for y in range(5):
        color = (255, 255, 255) if (x+y) % 2 == 0 else (255, 0, 0)
        pygame.draw.rect(background, color, (x*50, y*50, 50, 50))

size = background.get_size()
cropped_background = pygame.Surface(size, pygame.SRCALPHA)
pygame.draw.ellipse(cropped_background, (255, 255, 255, 255), (0, 0, *size))
cropped_background.blit(background, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    window.fill((0, 0, 0))
    window.blit(cropped_background, (0, 0))
    pygame.display.flip()