import pygame
from itertools import count


class VerletObject:
    objects_count = count()

    def __init__(self, x: int, y: int, radius: int = 15):
        self.id = next(self.objects_count)
        self.radius = radius

        self.currentPosition = pygame.Vector2(x, y)
        self.lastPosition = self.currentPosition
        self.acceleration = pygame.Vector2()

    def update_position(self, dt: float):
        velocity: pygame.math.Vector2 = self.currentPosition - self.lastPosition
        # Save the current position
        self.lastPosition = self.currentPosition
        # Perform Verlet integration
        self.currentPosition = self.currentPosition + velocity + self.acceleration * dt * dt
        # Reset acceleration
        self.acceleration = pygame.Vector2()

    def accelerate(self, acceleration: pygame.math.Vector2):
        self.acceleration += acceleration

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.currentPosition, self.radius)


class Link:
    def __init__(self, object1: VerletObject, object2: VerletObject, target_dist: float):
        self.object1 = object1
        self.object2 = object2
        self.target_dist = target_dist

    def apply(self):
        # Solve the constraint between the two objects
        axis: pygame.math.Vector2 = self.object1.currentPosition - self.object2.currentPosition # vector from object1 to object2
        dist = axis.length() # the actual distance
        n: pygame.math.Vector2 = axis / dist # normalized axis
        delta: float = self.target_dist - dist # the penetration depth
        self.object1.currentPosition += 0.5 * delta * n # move object1 half the penetration depth
        self.object2.currentPosition -= 0.5 * delta * n # move object2 half the penetration depth

    def draw(self):
        pygame.draw.line(pygame.display.get_surface(), (200, 200, 200), self.object1.currentPosition, self.object2.currentPosition, 2)


class Solver:
    def __init__(self, verlet_objects: list[VerletObject], links: list[Link]):
        self.verlet_objects = verlet_objects
        self.gravity: pygame.math.Vector2 = pygame.Vector2(0.0, 1000.0)

        self.links = links

    def update(self, dt: float):
        sub_steps = 8 # heavily impacts the stability of the simulation and the performance
        sub_dt = dt / float(sub_steps)
        for _ in range(sub_steps, 0, -1):
            # self.apply_gravity()
            self.apply_constraints_screen()
            self.solve_collisions()
            # self.update_positions(sub_dt)

            self.update_links() 

        self.draw_verlet_objects(pygame.display.get_surface())
        self.draw_links()

    def update_positions(self, dt: float):
        for verlet_object in self.verlet_objects:
            verlet_object.update_position(dt)

    def apply_gravity(self):
        for verlet_object in self.verlet_objects:
            verlet_object.accelerate(self.gravity)

    def apply_constraints_circle(self):
        screen_center = pygame.Vector2(pygame.display.get_surface().get_size()) // 2
        radius = 380
        pygame.draw.circle(pygame.display.get_surface(), (200, 200, 200), screen_center, radius, 2)
        for verlet_object in self.verlet_objects:
            to_obj = verlet_object.currentPosition - screen_center # vector from center to object
            dist = to_obj.length() # distance from center to object
            if dist > radius - verlet_object.radius:
                n = to_obj / dist # normalized vector from center to object
                verlet_object.currentPosition = screen_center + n * (radius - verlet_object.radius)

    def apply_constraints_circle_2(self):
        screen_center = pygame.Vector2(pygame.display.get_surface().get_size()) // 2
        radius = 380
        pygame.draw.circle(pygame.display.get_surface(), (200, 200, 200), screen_center, radius, 2)
        for verlet_object in self.verlet_objects:
            to_obj = verlet_object.currentPosition - screen_center
            dist = to_obj.length()
            if dist > radius - self.verlet_objects[0].radius:
                to_obj.scale_to_length(radius - self.verlet_objects[0].radius)
                verlet_object.currentPosition = screen_center + to_obj

    def apply_constraints_screen(self):
        screen_size = pygame.Vector2(pygame.display.get_surface().get_size())
        for verlet_object in self.verlet_objects:
            if verlet_object.currentPosition.x < verlet_object.radius:
                verlet_object.currentPosition.x = verlet_object.radius
            if verlet_object.currentPosition.x > screen_size.x - verlet_object.radius:
                verlet_object.currentPosition.x = screen_size.x - verlet_object.radius
            if verlet_object.currentPosition.y < verlet_object.radius:
                verlet_object.currentPosition.y = verlet_object.radius
            if verlet_object.currentPosition.y > screen_size.y - verlet_object.radius:
                verlet_object.currentPosition.y = screen_size.y - verlet_object.radius

    def solve_collisions(self):
        for verlet_object in self.verlet_objects:
            for other in self.verlet_objects:
                if verlet_object.id == other.id:
                    continue
                collision_axis = verlet_object.currentPosition - other.currentPosition
                dist = collision_axis.length()
                min_dist = verlet_object.radius + other.radius
                if dist < min_dist:
                    # one way
                    #if collision_axis.length_squared() > 0:
                    #    collision_axis.scale_to_length(min_dist)
                    #    verlet_object.currentPosition = other.currentPosition + collision_axis

                    # another way
                    #collision_axis.scale_to_length(verlet_object.radius + other.radius)
                    #verlet_object.currentPosition = other.currentPosition + collision_axis

                    n = collision_axis / dist # the normalized collision axis
                    delta = min_dist - dist # the penetration depth
                    verlet_object.currentPosition += 0.3 * delta * n # move verlet_object half the penetration depth, 0.3 or 0.5 is like a bounce factor

    def solve_collisions_2(self):
        for i in range(len(self.verlet_objects)):
            object1 = self.verlet_objects[i]
            for j in range(i + 1, len(self.verlet_objects)):
                object2 = self.verlet_objects[j]
                collision_axis = object1.currentPosition - object2.currentPosition
                dist = collision_axis.length() # the actual distance
                min_dist = object1.radius + object2.radius # the minimum distance
                if dist < min_dist:
                    n = collision_axis / dist # the normalized collision axis
                    delta = min_dist - dist # the penetration depth
                    object1.currentPosition += n * delta * 0.5

    def draw_verlet_objects(self, screen):

        for verlet_object in self.verlet_objects:
            verlet_object.draw(screen)

    def update_links(self): 
        for link in self.links:
            link.apply()

    def draw_links(self):
        for link in self.links:
            link.draw()