import pygame, random, sys, math

clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Sparks')
screen = pygame.display.set_mode((700, 600), 0, 32)

sparks = []

class Spark:
    def __init__(self, loc, angle, speed, color, scale) -> None:
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.color = color
        self.scale = scale
        self.alive = True

    def point_towards(self, angle, rate):
        rotate_direction = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
        try:
            rotate_sign = rotate_direction / abs(rotate_direction)
        except ZeroDivisionError:
            rotate_sign = 1
        if abs(rotate_direction) < rate: #> rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign # rotate_direction * rotate_sign

    def calculate_movement(self, dt):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]

    # gravity and friction
    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])
        # self.speed = math.sqrt(movement[0] ** 2 + movement[1] ** 2) # if you want to get more realistic

    def move(self, dt):
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0] # * 4
        self.loc[1] += movement[1] # * 4

        # a bunch of options to mess around relating to angles
        # self.point_towards(math.pi / 2, math.pi / 2 * dt)
        # self.velocity_adjust(0.975, 0.2, 8, dt)
        self.angle += 0.1

        self.speed -= 0.1

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf, offset):
        if self.alive:
            # sticks
            points = [
                [self.loc[0] + math.cos(self.angle) * self.speed * self.scale, self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
                [self.loc[0] + math.cos(self.angle + math.pi * 2) * self.speed * self.scale * 0.3, self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5, self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.loc[0] + math.cos(self.angle - math.pi * 2) * self.speed * self.scale * 0.3, self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
            ]
            
            # sparks
            points = [
                [self.loc[0] + math.cos(self.angle) * self.speed * self.scale, self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
                [self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3, self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5, self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3, self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
            ]
            pygame.draw.polygon(surf, self.color, points)


def main():
    font = pygame.font.SysFont('Arial', 20)
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
    while True:
        dt = clock.tick(60) / 1000
        screen.fill((0, 0, 0))

        for i, spark in sorted(enumerate(sparks), reverse=True):
            # spark.move(dt)
            spark.move(1)
            spark.draw(screen, [0, 0])
            if not spark.alive:
                sparks.pop(i)

        mx, my = pygame.mouse.get_pos()
        for i in range(100): 
            sparks.append(Spark([mx, my], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 2))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        n_particles = font.render(f'Particles: {len(sparks)}', True, (255, 255, 255))
        screen.blit(n_particles, (10, 10))
        fps = font.render(f'FPS: {int(clock.get_fps())}', True, (255, 255, 255))
        screen.blit(fps, (10, 30))

        pygame.display.flip()

if __name__ == '__main__':
    main()