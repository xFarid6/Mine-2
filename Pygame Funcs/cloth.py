from asyncio import events
import colorsys
import pygame


def hsv2rgb(h: float, s: float, v: float) -> tuple[int, ...]:
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

class Point:
    def __init__(self, x: int | float, y: int | float):
        """
        The function creates a class called Particle, which has the attributes x, y, oldx, oldy, ax, ay,
        mass, pin_x, and pin_y
        
        :param x: the x coordinate of the point
        :param y: the y coordinate of the point
        """
        # store prev and curr positions
        self.x = x
        self.y = y
        self.oldx = x
        self.oldy = y

        # the acceleration of the point is basically the gravity
        self.ax: float = 0
        self.ay: float = 1.0
        self.friction: float = 0.95

        self.mass: int = 10
        self.radius: int = 10
        self.pin_x: float | None = None
        self.pin_y: float | None = None

    def update(self) -> tuple[float, float]:
        """
        It updates the position of the point.
        :return: The x and y coordinates of the ball.
        """
        # if the point is pinned, then it returns the pin_x and pin_y values
        if self.pin_x is not None and self.pin_y is not None:
            return self.pin_x, self.pin_y
        
        # if the point is not pinned, then it updates the position of the point

        # the velocity of the point is calculated by subtracting the old position from the current position
        vx = (self.x - self.oldx) * self.friction 
        vy = (self.y - self.oldy) * self.friction

        # save the current position as the old position
        self.oldx = self.x
        self.oldy = self.y

        # update the position of the point by adding the velocity to the current position
        self.x += vx
        self.y += vy

        # update the position of the point by adding the acceleration to the current position
        self.x += self.ax
        self.y += self.ay

        # reset the acceleration to 0
        self.ax = 0
        self.ay = 1.5

        # multiply by dt^2, but dt is 1
        # self.x *= 1
        # self.y *= 1

        # return the x and y coordinates of the point
        return self.x, self.y

    def draw(self, screen: pygame.surface.Surface):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

    def add_force(self, fx: float, fy: float) -> None:
        """
        It adds force to the point.
        :param fx: the x component of the force
        :param fy: the y component of the force
        """
        self.ax += fx / self.mass
        self.ay += fy / self.mass

    def pin(self) -> None:
        """
        It pins the object to the screen.
        """
        self.pin_x = self.x
        self.pin_y = self.y

    def unpin(self) -> None:
        """
        It unpins the pin_x and pin_y values.
        """
        self.pin_x = None
        self.pin_y = None


class Stick:
    def __init__(self, p1: Point, p2: Point, target_length: int):
        """
        The function takes two points as input and returns the distance between them
        
        :param p1: The first point of the line
        :param p2: The point that the line is going to
        """
        self.p1 = p1
        self.p2 = p2
        self.length = target_length

        self.elasticity: float = 0.2

    def update(self) -> None:
        """
        If the points are not pinned, move them half the distance they are from the desired length
        """
        # distance between the two points on x and y
        dx = self.p1.x - self.p2.x
        dy = self.p1.y - self.p2.y

        # distance between the two points as value
        distance: float = (dx ** 2 + dy ** 2) ** 0.5

        # normalize the distance
        dx /= distance
        dy /= distance

        # calculate the difference between the distance and the target length
        difference = self.length - distance

        # move the points half the distance they are from the desired length
        if self.p1.pin_x is None and self.p1.pin_y is None:
            self.p1.x += dx * difference * self.elasticity
            self.p1.y += dy * difference * self.elasticity
        if self.p2.pin_x is None and self.p2.pin_y is None:
            self.p2.x -= dx * difference * self.elasticity
            self.p2.y -= dy * difference * self.elasticity

        """if not any((self.p1.pin_x, self.p1.pin_y, self.p2.pin_x, self.p2.pin_y)):
            self.p1.x += dx * difference * 0.5
            self.p1.y += dy * difference * 0.5
            self.p2.x -= dx * difference * 0.5
            self.p2.y -= dy * difference * 0.5
        if all((self.p1.pin_x, self.p1.pin_y)) and not any((self.p2.pin_x, self.p2.pin_y)):
            self.p2.x += dx * 2 
            self.p2.y += dy * 2 
        if all((self.p2.pin_x, self.p2.pin_y)) and not any((self.p1.pin_x, self.p1.pin_y)):
            self.p1.x -= dx * 2
            self.p1.y -= dy * 2"""

    def draw(self, screen: pygame.surface.Surface) -> None:
        pygame.draw.line(screen, (255, 255, 255), (int(self.p1.x), int(self.p1.y)), (int(self.p2.x), int(self.p2.y)), 1)


class Cloth:
    def __init__(self, x: int, y: int, width: int, height: int, side_size: int):
        """
        For each point in the grid, create a point, and then create sticks between the point and its
        neighbors.
        
        :param x: x coordinate of the top left corner of the cloth
        :param y: y-coordinate of the top left corner of the cloth
        :param w: width of the cloth
        :param h: height of the cloth
        :param res: number of points in each row/column
        """
        self.points: list[Point] = []
        self.sticks: list[Stick] = []
        target_distance: int = 30 # w / (res - 1)
        for j in range(side_size):
            for i in range(side_size):
                p = Point(x + i * width / side_size, y + j * height / side_size)
                self.points.append(p)
                if i > 0:
                    self.sticks.append(Stick(self.points[-1], self.points[-2], target_distance))
                if j > 0:
                    self.sticks.append(Stick(self.points[-1], self.points[-side_size - 1], target_distance))
                if i > 0 and j > 0:
                    self.sticks.append(Stick(self.points[-1], self.points[-side_size - 2], target_distance))
                    self.sticks.append(Stick(self.points[-2], self.points[-side_size - 1], target_distance))

        for i in range(side_size):
            self.points[i].pin()
            # self.points[-i - 1].pin()

    def update(self):
        """
        For each stick in the list of sticks, update the stick
        """
        for i in range(5):
            for s in self.sticks:
                s.update()
        for p in self.points:
            p.update()

    def draw(self, screen):
        """
        It draws the sticks and points of the stick figure
        
        :param screen: The screen to draw on
        """
        for s in self.sticks:
            s.draw(screen)
        for p in self.points:
            continue
            p.draw(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 700))
    pygame.display.set_caption("Cloth Simulation")
    clock = pygame.time.Clock()
    running = True

    cloth = Cloth(100, 10, 400, 400, 20)

    right = False
    left = False

    while running:
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w:
                    # add wind
                    for p in cloth.points:
                        p.add_force(0, 200)
                if event.key == pygame.K_a:
                    left = True
                if event.key == pygame.K_d:
                    right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    left = False
                if event.key == pygame.K_d:
                    right = False

        if left:
            """for p in cloth.points:
                p.add_force(-100, 0)"""
            for i in range(20):
                cloth.points[i].x -= 5

        if right:
            """for p in cloth.points:
                p.add_force(100, 0)"""
            for i in range(20):
                cloth.points[i].x += 5


        screen.fill((0, 0, 0))

        cloth.update()
        cloth.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
