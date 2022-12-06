import pygame
from settings import *
from quad_tree import QuadTree
from particle import Particle


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Width, Height))
        pygame.display.set_caption("Simulation")
        self.clock = pygame.time.Clock()
        self.running = True
        self.click = False

        Particle.img = Particle.img.convert_alpha()
        Particle.img = pygame.transform.scale(Particle.img, (Particle.radius, Particle.radius))
        self.tree = QuadTree(0, 0, Width, Height)

        self.particles = []

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont("comicsans", size, bold=True)
        text = font.render(text, False, color)
        self.screen.blit(text, (x, y))

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

    def update(self):
        if self.click:
            self.click = False
            self.tree.insert(Particle(*pygame.mouse.get_pos()))

        self.tree.update()

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.draw_text("FPS: " + str(int(self.clock.get_fps())), 10, (255, 255, 255), 10, 10)

        self.tree.draw(self.screen)

        pygame.display.flip()



if __name__ == '__main__':
    Main().run()