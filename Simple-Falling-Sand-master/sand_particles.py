import pygame
from dataclasses import dataclass, field
from verlet_sand import SandHolder, SandParticle, SandHolderDict


@dataclass(slots=True)
class Simulation:
    pygame.init()
    pygame.display.set_caption("Falling Sand")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    fps: int = 60

    mx: int = 0
    my: int = 0
    clicking: bool = False


    font = pygame.font.SysFont("Arial", 20)
    
    solver = SandHolderDict() # 200: no dict = 21 ; dict = 21
    solver.screen = screen
    
    def run(self):
        while 1:
            self.screen.fill((30, 30, 30))
            dt = self.clock.tick(self.fps) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False

            if self.clicking:
                self.solver.add_particle(pygame.mouse.get_pos())

            self.solver.update(dt)

            self.screen.blit(self.font.render(f"FPS: {self.clock.get_fps():.2f}", True, (255, 255, 255)), (10, 10))
            self.screen.blit(self.font.render(f"Particles: {len(self.solver.positions)}", True, (255, 255, 255)), (10, 30))

            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    Simulation().run()