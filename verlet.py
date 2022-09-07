from dataclasses import dataclass
import pygame


# here « velocity » is in fact the distance traveled since the last update so it’s already equivalent to velocity * dt

# A class that represents a Verlet object. It has a current position, an old position, an
# acceleration, and a radius. It has a method to update the position, and a method to accelerate the
# object.
@dataclass
class VerletObject:
    
    position_current: pygame.math.Vector2   
    position_old: pygame.math.Vector2
    acceleration: pygame.math.Vector2
    radius: float = 50


    def update_position(self, dt: float) -> None: 
        """
        > The current position is updated by adding the velocity (which is the difference between the
        current and previous position) to the current position, and then adding the acceleration multiplied
        by dt squared
        
        Args:
          dt (float): float = 0.01
        """
        velocity: pygame.math.Vector2 = self.position_current - self.position_old
        # Save current position
        self.position_old = self.position_current
        # Perform Verlet integration
        # multiplied by dt^2 because current_pos - last_pos is already equal to velocity 
        # dt (it's a distance, same unit as velocity dt)
        self.position_current = self.position_current + velocity + self.acceleration * dt * dt
        # Reset acceleration
        self.acceleration = pygame.math.Vector2()

    
    def accelerate(self, acc: pygame.math.Vector2) -> None:
        self.acceleration += acc 


class Solver:
    def __init__(self, physics_objects: list[VerletObject]):
        self.gravity: pygame.math.Vector2 = pygame.math.Vector2((0.0, 1000.0))
        self.physics_objects: list[VerletObject] = physics_objects

    
    def update(self, dt: float) -> None:
        sub_steps: int = 2
        sub_dt: float = dt / float(sub_steps)
        for i in range(sub_steps, 0):
            self.apply_gravity()
            self.apply_constraint()
            self.solve_collisions()
            self.update_positions(sub_dt)

    
    def update_positions(self, dt: float) -> None:
        for verletObj in self.physics_objects:
            verletObj.update_position(dt)


    def apply_gravity(self) -> None:
        for verletObj in self.physics_objects:
            verletObj.accelerate(self.gravity)

    
    def apply_constraint(self) -> None:
        position: pygame.math.Vector2 = pygame.math.Vector2((800.0, 450.0))
        radius: float = 400.0
        for verletObj in self.physics_objects:
            to_obj: pygame.math.Vector2 = verletObj.position_current - position
            dist: float = to_obj.length()
            # 50 is the default radius
            if dist > radius - 50.0:
                n: pygame.math.Vector2 = to_obj / dist
                verletObj.position_current = position + n * (radius - 50.0) # (dist - 50.0)

    
    def solve_collisions(self) -> None:
        object_count: int = len(self.physics_objects)
        object_container = self.physics_objects
        for i in range(object_count): 
            object_1: VerletObject = object_container[i]
            for k in range(i+1, object_count):
                object_2: VerletObject = object_container[k]
                collsion_axis: pygame.math.Vector2 = object_1.position_current - object_2.position_current
                dist: float = collsion_axis.length()
                if dist < 100.0:
                    n: pygame.math.Vector2 = collsion_axis / dist
                    delta: float = 100.0 - dist
                    object_1.position_current += 0.5 * delta * n


class Link:
    def __init__(self, object_1: VerletObject, object_2: VerletObject):
        self.object_1: VerletObject = object_1
        self.object_2: VerletObject = object_2
        self.target_distance: float

    
    def apply(self):
        obj_1 = self.object_1
        obj_2 = self.object_2
        axis: pygame.math.Vector2 = obj_1.position_current - obj_2.position_current
        dist: float = axis.length()
        n: pygame.math.Vector2 = axis / dist
        delta: float =  self.target_distance - dist
        obj_1.position_current += 0.5 * delta * n
        obj_2.position_current -= 0.5 * delta * n

################################################################

"""
Checking out wind.hpp at https://github.com/johnBuffer/ClothSimulation/blob/main/include/wind.hpp

there is a wind struct, 
oddly similar to a rect, with just an update method that moves the rect.left 
by a force multiplied by dt and an arbitrary value

and there is a struct wind manager,
which takes a vector of winds; it has an update method that is used to call
the update method on each of the Wind in the vector
and moves all the particles in the wind area by a certain force
and if the wind rect is going over the screen it resets its width to 0

seems like to solvers take in a vector of something and update every parameter of each of the 
objects in the vector.
example: for every object that has physics there is a physics solver that updates:
            applyGravity();
            applyAirFriction();
            updatePositions(sub_step_dt);
            solveConstraints();
            updateDerivatives(sub_step_dt);
"""