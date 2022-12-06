import pygame
from settings import *
from particle import Particle
import random


class Node:
    def __init__(self, parent, x: int, y: int, width: int, height: int, capacity: int) -> None:
        # node linked up
        self.parent = parent

        # area they cover
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # how many particles can be in this node
        self.capacity = capacity
        # how many particles are in this node
        self.particles = set()

        # children
        self.northWest: Node | None = None
        self.northEast: Node | None = None
        self.southWest: Node | None = None 
        self.southEast: Node | None = None

        # color
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), 
                                    (255, 255, 0), (255, 0, 255), (0, 255, 255), 
                                    (200, 255, 100), (0, 0, 0), (128, 128, 128)])

    def get_particles(self) -> set:
        return self.particles

    # return true if it has children
    def is_divided(self) -> bool:
        return not self.northWest is None

    def is_empty(self) -> bool:
        return len(self.particles) == 0

class QuadTree:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.root = Node(None, x, y, width, height, ParticlesPerNode)


    def insert(self, particle: Particle) -> None:
        self.insert_particle(self.root, particle)

    def insert_particle(self, node: Node, particle: Particle) -> bool:
        # if the node does not contain the particle, return
        if not self.contains(node, particle):
            node.particles.discard(particle)
            return False 

        # if the node has space for the particle, add it
        if len(node.particles) < node.capacity and not node.is_divided():
            node.particles.add(particle)
            return True
        
        # if the node is not divided, divide it
        if not node.is_divided():
            self.divide(node)

        # if the node is divided, add the particle to the correct child
        if self.insert_particle(node.northWest, particle):
            return True
        if self.insert_particle(node.northEast, particle):
            return True
        if self.insert_particle(node.southWest, particle):
            return True
        if self.insert_particle(node.southEast, particle):
            return True

        return False

    def contains(self, node: Node, particle: Particle) -> bool:
        return (
             node.x <= particle.x <= node.x + node.width
            ) and (
                node.y <= particle.y <= node.y + node.height
                )

    def divide(self, node: Node) -> None:
        # create the children
        node.northWest = Node(node, node.x, node.y, int(node.width/2), int(node.height/2), node.capacity)
        node.northEast = Node(node, int(node.x + node.width/2), node.y, int(node.width/2), int(node.height/2), node.capacity)
        node.southWest = Node(node, node.x, int(node.y + node.height/2), int(node.width/2), int(node.height/2), node.capacity)
        node.southEast = Node(node, int(node.x + node.width/2), int(node.y + node.height/2), int(node.width/2), int(node.height/2), node.capacity)
   
        # move the particles to the children
        for particle in node.particles.copy():
            self.insert_particle(node, particle)

        # clear the particles from the parent
        # node.particles.clear()


    def update(self):
        particles = self.get_particles()
        for particle in particles.copy():
            particle.update()
            self.insert(particle)
            self.handle_collisions(self.root)

        self.delete_empty_nodes(self.root)

    def delete_empty_nodes(self, node: Node) -> None:
        """Delete all the empty nodes in the tree"""
        if node.is_divided():
            self.delete_empty_nodes(node.northWest)
            self.delete_empty_nodes(node.northEast)
            self.delete_empty_nodes(node.southWest)
            self.delete_empty_nodes(node.southEast)

        if node.parent is None:
            return

        if all([node.parent.northWest.is_empty(), node.parent.northEast.is_empty(), node.parent.southWest.is_empty(), node.parent.southEast.is_empty()]):
            op_node = node.parent
            op_node.northWest = None
            op_node.northEast = None
            op_node.southWest = None
            op_node.southEast = None

    def handle_collisions(self, node: Node) -> None:
        """Handle collisions in the tree"""
        if node.is_divided():
            self.handle_collisions(node.northWest)
            self.handle_collisions(node.northEast)
            self.handle_collisions(node.southWest)
            self.handle_collisions(node.southEast)

        for particle in node.particles.copy():
            for other_particle in node.particles.copy():
                if particle == other_particle:
                    continue

                collision_axis: pygame.math.Vector2 = pygame.math.Vector2(particle.x - other_particle.x, particle.y - other_particle.y)
                distance = collision_axis.length() if collision_axis.length() != 0 else 0.0001
                if distance < particle.radius + other_particle.radius:
                    n = collision_axis / distance
                    delta = (particle.radius + other_particle.radius) - distance
                    particle.x += n.x * delta * 0.5
                    particle.y += n.y * delta * 0.5

    def draw(self, screen: pygame.surface.Surface) -> None:
        self.draw_node(screen, self.root)
        self.draw_particles(screen, self.root)

    def draw_node(self, screen: pygame.surface.Surface, node: Node) -> None:
        if node.is_divided():
            self.draw_node(screen, node.northWest)
            self.draw_node(screen, node.northEast)
            self.draw_node(screen, node.southWest)
            self.draw_node(screen, node.southEast)

        pygame.draw.rect(screen, (255, 255, 255), (node.x, node.y, node.width, node.height), 1)

    def draw_particles(self, screen: pygame.surface.Surface, node: Node) -> None:
        if node.is_divided():
            self.draw_particles(screen, node.northWest)
            self.draw_particles(screen, node.northEast)
            self.draw_particles(screen, node.southWest)
            self.draw_particles(screen, node.southEast)

        for particle in node.particles:
            particle.draw(screen)
            pygame.draw.circle(screen, node.color, (particle.x, particle.y), particle.radius, 4)


    def get_particles(self) -> set:
        """Get all the particles in the tree"""
        return self.get_particles_node(self.root)

    def get_particles_node(self, node: Node) -> set:
        """Get all the particles in the node"""
        if node.is_divided():
            '''return (
                self.get_particles_node(node.northWest)
                + self.get_particles_node(node.northEast)
                + self.get_particles_node(node.southWest)
                + self.get_particles_node(node.southEast)
                )'''
            return (
                self.get_particles_node(node.northWest)
                | self.get_particles_node(node.northEast)
                | self.get_particles_node(node.southWest)
                | self.get_particles_node(node.southEast)
                )

        return node.particles


    def query(self, x: int, y: int, width: int, height: int) -> set:
        """Get all the particles in the area"""
        return self.query_node(self.root, x, y, width, height)

    def query_node(self, node: Node, x: int, y: int, width: int, height: int) -> set:
        """Get all the particles in the node in the area"""
        # if the node does not intersect the area, return
        if not self.intersects(node, x, y, width, height):
            return []

        # if the node is divided, query the children
        if node.is_divided():
            '''return (
                self.query_node(node.northWest, x, y, width, height)
                + self.query_node(node.northEast, x, y, width, height)
                + self.query_node(node.southWest, x, y, width, height)
                + self.query_node(node.southEast, x, y, width, height)
                )'''
            return (
                self.query_node(node.northWest, x, y, width, height)
                | self.query_node(node.northEast, x, y, width, height)
                | self.query_node(node.southWest, x, y, width, height)
                | self.query_node(node.southEast, x, y, width, height)
                )

        # if the node is not divided, return the particles
        return node.particles

    def intersects(self, node: Node, x: int, y: int, width: int, height: int) -> bool:
        return (
            node.x <= x + width and node.x + node.width >= x
                ) and (
                    node.y <= y + height and node.y + node.height >= y
                        )



if __name__ == "__main__":
    from main import Main

    Main().run()