from collections import defaultdict
from dataclasses import dataclass, field
from math import dist
from pprint import pprint
import pygame
from itertools import count


class SandParticle:

    id_iter = count()

    # create a particle with physics calculated with Verlet integration
    def __init__(self):

        self.id = next(self.id_iter)


@dataclass(slots=True)
class SandHolder:
    particles: list[SandParticle] = field(default_factory=list)

    positions: list[list[int | float]] = field(default_factory=list)
    old_positions: list[list[int | float]] = field(default_factory=list)
    accelerations: list[list[int | float]] = field(default_factory=list)

    mass: int = 3
    radius: int = 20
    color: tuple[int, int, int] = (255, 255, 255)
    friction: float = 0.9999
    gravity: list[float] = field(default_factory=lambda: [0.0, 1000.0])

    screen: pygame.surface.Surface = field(default_factory=pygame.display.get_surface)
    width, height = 800, 600

    adjacents: list[list[int]] = field(default_factory=list)

    def apply_verlet(self, dt):
        # update the position of the particle with verlet
        for particle in self.particles:
            # get id of particle
            idx = particle.id

            # calculate velocity and apply friction
            velocity_x = (self.positions[idx][0] - self.old_positions[idx][0]) * self.friction
            velocity_y = (self.positions[idx][1] - self.old_positions[idx][1]) * self.friction

            # save current position
            self.old_positions[idx][0] = self.positions[idx][0]
            self.old_positions[idx][1] = self.positions[idx][1]

            # perform verlet integration
            self.positions[idx][0] += velocity_x + self.accelerations[idx][0] * dt * dt
            self.positions[idx][1] += velocity_y + self.accelerations[idx][1] * dt * dt

            # reset acceleration
            self.accelerations[idx][0] = 0
            self.accelerations[idx][1] = 0

    def apply_forces(self, force):
        # apply a force to the particle
        for particle in self.particles:
            idx = particle.id
            self.accelerations[idx][0] += force[0] / self.mass
            self.accelerations[idx][1] += force[1] / self.mass

    def draw(self, screen):
        # draw the particle
        for particle in self.particles:
            idx = particle.id
            pygame.draw.circle(screen, self.color, (self.positions[idx][0], self.positions[idx][1]), self.radius)

    def constrain_in_screen(self):
        # constrain the particle in the screen
        for particle in self.particles:
            idx = particle.id
            pos_list = self.positions[idx]
            if pos_list[0] < 0 + self.radius:
                pos_list[0] = self.radius
            elif pos_list[0] > self.width - self.radius:
                pos_list[0] = self.width - self.radius

            if pos_list[1] < 0 + self.radius:
                pos_list[1] = self.radius
            elif pos_list[1] > self.height - self.radius:
                pos_list[1] = self.height - self.radius

    def constrain_in_circle(self):
        # constrain the particle in a circle
        center_circle = [self.width / 2, self.height / 2]
        radius_circle = 200
        for particle in self.particles:
            idx = particle.id
            pos_list = self.positions[idx]
            distance = dist(pos_list, center_circle)
            if distance > radius_circle:
                pos_list[0] = center_circle[0] + (pos_list[0] - center_circle[0]) * radius_circle / distance
                pos_list[1] = center_circle[1] + (pos_list[1] - center_circle[1]) * radius_circle / distance

        pygame.draw.circle(self.screen, (255, 255, 255), center_circle, radius_circle, 1)           

    def solve_collisions(self):
        # solve collisions between particles
        for particle in self.particles:
            idx = particle.id
            for other_particle in self.particles[idx+1:]:
                idx2 = other_particle.id
                collision_axis = [self.positions[idx][0] - self.positions[other_particle.id][0], self.positions[idx][1] - self.positions[other_particle.id][1]]
                distance = dist(self.positions[idx], self.positions[idx2])
                min_dist = self.radius * 2
                if distance < min_dist:
                    # solve collision
                    norm_coll_axis = [collision_axis[0] / distance, collision_axis[1] / distance]
                    delta = min_dist - distance
                    self.positions[idx][0] += norm_coll_axis[0] * delta * 0.4
                    self.positions[idx][1] += norm_coll_axis[1] * delta * 0.4
                    self.positions[idx2][0] -= norm_coll_axis[0] * delta * 0.4
                    self.positions[idx2][1] -= norm_coll_axis[1] * delta * 0.4

    def add_particle(self, pos):
        # add a particle to the simulation
        self.particles.append(SandParticle())
        self.positions.append(list(pos))
        self.old_positions.append(list(pos))
        self.accelerations.append([0, 0])

    def update(self, dt: float):

        sub_steps = 5 # heavily impacts the stability of the simulation and the performance
        sub_dt = dt / float(sub_steps)
        for _ in range(sub_steps, 0, -1):
            self.apply_forces(self.gravity)
            self.constrain_in_screen()
            self.solve_collisions()
            self.apply_verlet(sub_dt)

        self.draw(self.screen)


# remake the class SandHolder but make it use dictionaries instead of lists for every attribute
@dataclass(slots=True)
class SandHolderDict:
    id_iter = count()

    positions: dict[int, list[int | float]] = field(default_factory=dict)
    old_positions: dict[int, list[int | float]] = field(default_factory=dict)
    accelerations: dict[int, list[int | float]] = field(default_factory=dict)

    mass: int = 1
    radius: int = 30
    color: tuple[int, int, int] = (255, 255, 255)
    friction: float = 0.9999
    gravity: list[float] = field(default_factory=lambda: [0.0, 1000.0])

    screen: pygame.surface.Surface = field(default_factory=pygame.display.get_surface)
    width, height = 800, 600

    loc_strings: dict[int, str] = field(default_factory=dict)
    tile_map: dict[str, list] = field(default_factory=dict)
    tile_size: int = radius * 2
    
    def __post_init__(self):
        # simulate a grid of squares the size of the diameter of the particles
        for y in range(0, self.height+1):
            y1 = y // self.tile_size
            for x in range(0, self.width+1):
                x1 = x // self.tile_size
                self.tile_map[f'{x1},{y1}'] = []

        # pprint(self.tile_map)

    def apply_verlet(self, dt):
        # update the position of the particle with verlet
        for idx in range(len(self.positions)):

            # calculate velocity and apply friction
            velocity_x = (self.positions[idx][0] - self.old_positions[idx][0]) * self.friction
            velocity_y = (self.positions[idx][1] - self.old_positions[idx][1]) * self.friction

            # save current position
            self.old_positions[idx][0] = self.positions[idx][0]
            self.old_positions[idx][1] = self.positions[idx][1]

            # perform verlet integration
            self.positions[idx][0] += velocity_x + self.accelerations[idx][0] * dt * dt
            self.positions[idx][1] += velocity_y + self.accelerations[idx][1] * dt * dt

            # reset acceleration
            self.accelerations[idx][0] = 0
            self.accelerations[idx][1] = 0

    def apply_forces(self, force):
        # apply a force to the particle
        for k, v in self.accelerations.items():
            v[0] += force[0] / self.mass
            v[1] += force[1] / self.mass

    def draw(self, screen):
        # draw the particle
        for k, v in self.positions.items():
            pygame.draw.circle(screen, self.color, (int(v[0]), int(v[1])), self.radius)

    def constrain_in_screen(self):
        # constrain the particle in the screen
        for idx in range(len(self.positions)):
            pos_list = self.positions[idx]
            if pos_list[0] < 0 + self.radius:
                pos_list[0] = self.radius
            elif pos_list[0] > self.width - self.radius:
                pos_list[0] = self.width - self.radius

            if pos_list[1] < 0 + self.radius:
                pos_list[1] = self.radius
            elif pos_list[1] > self.height - self.radius:
                pos_list[1] = self.height - self.radius

    def solve_collisions(self):
        # solve collisions between particles
        """for idx in range(len(self.positions)):
            for idx2 in range(idx, len(self.positions)):
                if idx == idx2:
                    continue
                collision_axis = [self.positions[idx][0] - self.positions[idx2][0], self.positions[idx][1] - self.positions[idx2][1]]
                distance = dist(self.positions[idx], self.positions[idx2])
                min_dist = self.radius * 2
                if distance < min_dist:
                    # solve collision
                    norm_coll_axis = [collision_axis[0] / distance, collision_axis[1] / distance]
                    delta = min_dist - distance
                    self.positions[idx][0] += norm_coll_axis[0] * delta * 0.4
                    self.positions[idx][1] += norm_coll_axis[1] * delta * 0.4
                    self.positions[idx2][0] -= norm_coll_axis[0] * delta * 0.4
                    self.positions[idx2][1] -= norm_coll_axis[1] * delta * 0.4
                    self.positions[idx] = [self.positions[idx][0], self.positions[idx][1]]
                    self.positions[idx2] = [self.positions[idx2][0], self.positions[idx2][1]]"""

        # calculate and store in which cell each particle is
        for k, v in self.positions.items():
            x, y = v
            loc_str = f"{int(x // self.tile_size)},{int(y // self.tile_size)}" # cell location
            self.loc_strings[k] = loc_str # store the cell location of the particle
            # store the particle in the cell and remove duplicates
            self.tile_map[loc_str] = list(set(self.tile_map[loc_str] + [k]))

        # check positoins of all particles
        for k, v in self.positions.items():
            x, y = v
            loc_str = self.loc_strings[k] # extract the cell location of the particle
            
            if len(self.tile_map[loc_str]) > 1: # it will be in the tilemap at least once, so if there is more than one, there is a collision
                key1 = k # the first particle
                key2 = self.tile_map[loc_str][1] # the second particle
                collision_axis = [self.positions[key1][0] - self.positions[key2][0], self.positions[key1][1] - self.positions[key2][1]]
                distance = dist(self.positions[key1], self.positions[key2]) if dist(self.positions[key1], self.positions[key2]) > 0 else 1
                min_dist = self.radius * 2
                if distance < min_dist:
                    # solve collision
                    norm_coll_axis = [collision_axis[0] / distance, collision_axis[1] / distance]
                    delta = min_dist - distance
                    self.positions[key1][0] += norm_coll_axis[0] * delta * 0.4
                    self.positions[key1][1] += norm_coll_axis[1] * delta * 0.4
                    self.positions[key2][0] -= norm_coll_axis[0] * delta * 0.4
                    self.positions[key2][1] -= norm_coll_axis[1] * delta * 0.4
                    self.positions[key1] = [self.positions[key1][0], self.positions[key1][1]]
                    self.positions[key2] = [self.positions[key2][0], self.positions[key2][1]]

    def add_particle(self, pos):
        # add a particle to the simulation

        idx = next(self.id_iter)
        self.positions[idx] = list(pos)
        self.old_positions[idx] = list(pos)
        self.accelerations[idx] = [0, 0]

    def update(self, dt: float):
            
        sub_steps = 5
        sub_dt = dt / float(sub_steps)
        for _ in range(sub_steps, 0, -1):
            self.apply_forces(self.gravity)
            self.constrain_in_screen()
            self.solve_collisions()
            self.apply_verlet(sub_dt)

        self.draw(self.screen)


class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = defaultdict(set)

    def get_cell(self, pos):
        return pos[0] // self.cell_size, pos[1] // self.cell_size

    def add(self, pos, idx):
        cell = self.get_cell(pos)
        self.grid[cell].add(idx)

    def get_adjacents(self, pos):
        cell = self.get_cell(pos)
        adjacents = set()
        for x in range(-1, 2):
            for y in range(-1, 2):
                adjacents.update(self.grid[cell[0] + x, cell[1] + y])
        return adjacents

    def update(self, positions):
        self.grid.clear()
        for idx, pos in positions.items():
            self.add(pos, idx)
            