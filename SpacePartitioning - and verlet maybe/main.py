import time
import pygame
import random
from particle import Particle
from quadtree import QuadTree, Rectangle, Point, Circle


class Game:
    def __init__(self)  -> None:
        pygame.init()
        self.Width: int = 1000
        self.Height: int = 800
        self.bg_color: tuple[int, int, int] = (30, 30, 30)

        self.screen: pygame.surface.Surface = pygame.display.set_mode((self.Width, self.Height))
        self.clock = pygame.time.Clock()
        self.running: bool = True

        self.spawn = False
        self.particles: list[Particle] = []
        self.setup()

        self.qtree: QuadTree

    def setup(self):
        boundary = Rectangle(0, 0, self.Width, self.Height)
        self.qtree = QuadTree(boundary=boundary, capacity=4)

        for _ in range(5):
            self.particles.append(Particle(x = random.randint(20, self.Width - 20), y = random.randint(20, self.Height - 20)))

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.spawn = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.spawn = False

    def update(self):
        self.qtree = QuadTree(Rectangle(0, 0, self.Width, self.Height), 4)
        # self.qtree.clear()
        for particle in self.particles:
            particle.apply_force(particle.gravity)
            particle.move()
            particle.constraints_C()
            self.qtree.insert(Point(particle.x, particle.y, particle))

        if self.spawn:
            self.particles.append(Particle(x = pygame.mouse.get_pos()[0], y = pygame.mouse.get_pos()[1]))
            # self.spawn = False

    def draw(self):
        self.screen.fill(self.bg_color)

        for particle in self.particles:
            particle.draw()
            # particle.set_higlihted(False)

        for particle in self.particles:
            circle = Circle(particle.x, particle.y, particle.radius*2)
            points = self.qtree.query(circle, [])
            for point in points:
                other = point.userData
                if particle.intersects(other) and particle != other:
                    # particle.set_higlihted(True)
                    particle.verlet(other)

        self.draw_text("FPS: " + str(int(self.clock.get_fps())), 20, (255, 0, 0), 10, 10)
        self.draw_text("Particles: " + str(len(self.particles)), 20, (255, 0, 0), 10, 30)

        pygame.draw.circle(self.screen, (255, 255, 255), (self.Width //2, self.Height//2), 300, 1)

        self.qtree.show(self.screen)

        pygame.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont("comicsans", size)
        text = font.render(text, True, color)
        self.screen.blit(text, (x, y))


if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()