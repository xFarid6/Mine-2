from __future__ import annotations
import math
import random
import pygame
from enum import Enum, auto

# file settings, contains globals
ENABLE_AUTO_COLLISION_DETECTION: bool = True
ENABLE_AUTO_COLLISION_REACTION: bool = True
FIRE_PARTICLE_LIFETIME: int = 100
RAIN_PARTICLE_LIFETIME: int = 1000
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
EXPLOSION_PARTICLE_LIFETIME: int = 100
SMOKE_PARTICLE_LIFETIME: int = 100

# file Point2D (vectors essentially)
class Point2D:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def create(self, x: float, y: float):
        return Point2D(x, y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point2D({self.x}, {self.y})"

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point2D(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Point2D(self.x / other, self.y / other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError("Index out of range")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Index out of range")

    def __len__(self):
        return 2

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __neg__(self):
        return Point2D(-self.x, -self.y)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __round__(self, n=None):
        return Point2D(round(self.x, n), round(self.y, n))

    def __floor__(self):
        return Point2D(self.x // 1, self.y // 1)

    def __ceil__(self):
        return Point2D(self.x // 1 + 1, self.y // 1 + 1)

    def __trunc__(self):
        return Point2D(self.x // 1, self.y // 1)

    def __copy__(self):
        return Point2D(self.x, self.y)

    def __deepcopy__(self, memodict={}):
        return Point2D(self.x, self.y)

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __le__(self, other):
        return abs(self) <= abs(other)

    def __gt__(self, other):
        return abs(self) > abs(other)

    def __ge__(self, other):
        return abs(self) >= abs(other)

    def __contains__(self, item):
        return item in (self.x, self.y)

    def __format__(self, format_spec):
        return f"({self.x:{format_spec}}, {self.y:{format_spec}})"

    def __dir__(self):
        return ["x", "y"]

    def __getattribute__(self, item):
        if item == "x":
            return super().__getattribute__(item)
        elif item == "y":
            return super().__getattribute__(item)
        else:
            raise AttributeError(f"Point2D has no attribute {item}")

    def __setattr__(self, key, value):
        if key == "x":
            super().__setattr__(key, value)
        elif key == "y":
            super().__setattr__(key, value)
        else:
            raise AttributeError(f"Point2D has no attribute {key}")

    def __delattr__(self, item):
        if item == "x":
            super().__delattr__(item)
        elif item == "y":
            super().__delattr__(item)
        else:
            raise AttributeError(f"Point2D has no attribute {item}")

    def __getnewargs__(self):
        return self.x, self.y

    def __getstate__(self):
        return self.x, self.y

    def __setstate__(self, state):
        self.x, self.y = state

    def __reduce__(self):
        return Point2D, self.__getstate__()

    def __reduce_ex__(self, protocol):
        return Point2D, self.__getstate__()

    def __sizeof__(self):
        return 16

    def __call__(self, *args, **kwargs):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __await__(self):
        yield self

    def __aiter__(self):
        return self

    def __anext__(self):
        return self


# file game_object_base
class CollisionType(Enum):
    NONE = auto()
    CIRCLE = auto()
    POLY = auto()


class GameObjectBase:

    def __init__(self): 
        self.engine: EngineBase 

        self.position: Point2D
        self.speed: Point2D

        self.rotation_angle: float
        self.old_rotation_angle: float
        self.rotationSpeed: float

        # Collision Detection
        self.collision_type: CollisionType = CollisionType.NONE
        self.collision_circle_radius: float = 0.0
        self.collision_poly_points: list[Point2D] = []
        self.no_collision_points: int = 0
        self.rotated_collision_poly_points: list[Point2D] = []
        self.auto_collision_detected: list[GameObjectBase] = []
        self.auto_collision_details: list[CollisionDetails] = []

    def logic(self, dt: float) -> None:
        ...

    def draw(self, surface: pygame.Surface) -> None:
        ...

    def get_position(self) -> Point2D:
        return self.position

    def get_rotation_angle(self) -> float:
        return self.rotation_angle

    def get_collision_type(self) -> CollisionType:
        return self.collision_type

    def get_collision_circle_radius(self) -> float:
        return self.collision_circle_radius

    def get_collision_poly_points(self) -> list[Point2D]:
        return self.collision_poly_points

    def get_no_collision_poly_points(self) -> int:
        return self.no_collision_points

    def get_rotated_collision_poly_points(self) -> list[Point2D]:
        return self.rotated_collision_poly_points

    def clear_auto_collisions(self) -> None:
        self.auto_collision_detected.clear()

    def calculate_rotated_collision_poly_points(self) -> None:
        if self.old_rotation_angle != self.rotation_angle:
            for i in range(self.no_collision_points):
                self.rotated_collision_poly_points.append(
                    Point2D(
                        self.collision_poly_points[i].x * math.cos(self.rotation_angle) - self.collision_poly_points[i].y * math.sin(self.rotation_angle),
                        self.collision_poly_points[i].x * math.sin(self.rotation_angle) + self.collision_poly_points[i].y * math.cos(self.rotation_angle)
                    )
                )

            self.old_rotation_angle = self.rotation_angle

    def add_auto_collision(self, game_object: GameObjectBase, collisionDetails: CollisionDetails) -> None:
        self.auto_collision_detected.append(game_object)
        self.auto_collision_details.append(collisionDetails)

    def react_to_collisions(self, dt: float) -> None:
        if self.collision_type == CollisionType.CIRCLE:
            for collision in self.auto_collision_details:
                self.position.x += collision.reaction_vector_object1.x
                self.position.y += collision.reaction_vector_object1.y
                self.speed.x += collision.reaction_vector_object1.x / dt
                self.speed.y += collision.reaction_vector_object1.y / dt

        if self.collision_type == CollisionType.POLY:
            collision_cls_instance: Collisions = Collisions()
            for collision in self.auto_collision_details:
                
                centerAx: Point2D = Point2D(-collision.collision_point_object1.x, -collision.collision_point_object1.y)
                centerPP: Point2D = Point2D(collision.collision_point_object1.y, -collision.collision_point_object1.x)

                speedChange: Point2D = collision_cls_instance.get_projected_point_on_line(collision.reaction_vector_object1, centerAx)
                self.position.x += speedChange.x
                self.position.y += speedChange.y
                self.speed.x += speedChange.x * dt * 50
                self.speed.y += speedChange.y * dt * 50

                rotationChangePoint: Point2D = collision_cls_instance.get_projected_point_on_line(collision.reaction_vector_object1, centerPP)
                rotationChangeAmount: float = math.sqrt(pow(rotationChangePoint.x, 2) + pow(rotationChangePoint.y, 2))
                if collision_cls_instance.dot_product(centerPP, rotationChangePoint) > 0:
                    rotationChangeAmount *= -1

                self.rotationSpeed += rotationChangeAmount * dt * 2

# file engine base    
class EngineBase:
    def __init__(self) -> None:
        self.game_objects: list[GameObjectBase] = []
        self.mouse_position: Point2D

    def set_mouse_position(self, x: int, y: int) -> None:
        self.mouse_position.x = x
        self.mouse_position.y = y

    def get_mouse_position(self) -> Point2D:
        return self.mouse_position

    def logic(self, dt: float) -> None:
        for object in self.game_objects:
            object.logic(dt)
            if object.get_collision_type() == CollisionType.POLY:
                object.calculate_rotated_collision_poly_points()

        # Auto collision detection
        if ENABLE_AUTO_COLLISION_DETECTION:
            for game_object in self.game_objects:
                game_object.clear_auto_collisions()
            
            for i, game_object in enumerate(self.game_objects):
                if game_object.get_collision_type() != CollisionType.NONE:
                    for game_object2 in self.game_objects[i:]:
                        if game_object2.get_collision_type() != CollisionType.NONE:
                            collisions = Collisions()
                            collision_details: CollisionDetails = collisions.objects_collide(game_object, game_object2)
                            if collision_details.collides:
                                game_object.add_auto_collision(game_object2, collision_details)
                                collision_details.swap_objects()
                                game_object2.add_auto_collision(game_object, collision_details)

        # React to collisions
        if ENABLE_AUTO_COLLISION_REACTION:
            for game_object in self.game_objects:
                game_object.react_to_collisions(dt)


    def draw(self, surface: pygame.Surface) -> None:
        for object in self.game_objects:
            object.draw(surface)

    def add_game_object(self, game_object: GameObjectBase) -> None:
        self.game_objects.append(game_object)

    def remove_game_object(self, game_object: GameObjectBase) -> None:
        self.game_objects.remove(game_object)

    def key_up(self, key: int) -> None:
        ...

    def key_down(self, key: int) -> None:
        ...

    def mouse_button_up(self, left: bool, right: bool) -> None:
        ...

    def mouse_button_down(self, left: bool, right: bool) -> None:
        ...


# file collisions.h, collisions.cpp
"""class CollisionsGitHubCopilot:
    def __init__(self) -> None:
        ...

    def check_collision(self, game_object: GameObjectBase) -> None:
        if game_object.get_collision_type() == CollisionType.CIRCLE:
            self.check_circle_collision(game_object)
        elif game_object.get_collision_type() == CollisionType.POLY:
            self.check_poly_collision(game_object)

    def check_circle_collision(self, game_object: GameObjectBase) -> None:
        for other_object in game_object.engine.game_objects:
            if other_object != game_object:
                if other_object.get_collision_type() == CollisionType.CIRCLE:
                    self.check_circle_circle_collision(game_object, other_object)
                elif other_object.get_collision_type() == CollisionType.POLY:
                    self.check_circle_poly_collision(game_object, other_object)

    def check_circle_circle_collision(self, game_object: GameObjectBase, other_object: GameObjectBase) -> None:
        if game_object.get_position().distance(other_object.get_position()) <= game_object.get_collision_circle_radius() + other_object.get_collision_circle_radius():
            game_object.add_auto_collision(other_object)
            other_object.add_auto_collision(game_object)

    def check_circle_poly_collision(self, game_object: GameObjectBase, other_object: GameObjectBase) -> None:
        for i in range(other_object.get_no_collision_poly_points()):
            if game_object.get_position().distance(other_object.get_rotated_collision_poly_points()[i]) <= game_object.get_collision_circle_radius():
                game_object.add_auto_collision(other_object)
                other_object.add_auto_collision(game_object)
                break

    def check_poly_collision(self, game_object: GameObjectBase) -> None:
        for other_object in game_object.engine.game_objects:
            if other_object != game_object:
                if other_object.get_collision_type() == CollisionType.CIRCLE:
                    self.check_circle_poly_collision(other_object, game_object)
                elif other_object.get_collision_type() == CollisionType.POLY:
                    self.check_poly_poly_collision(game_object, other_object)

    def check_poly_poly_collision(self, game_object: GameObjectBase, other_object: GameObjectBase) -> None:
        for i in range(game_object.get_no_collision_poly_points()):
            if self.is_point_in_poly(game_object.get_rotated_collision_poly_points()[i], other_object.get_rotated_collision_poly_points()):
                game_object.add_auto_collision(other_object)
                other_object.add_auto_collision(game_object)
                break

    def is_point_in_poly(self, point: Point2D, poly: list[Point2D]) -> bool:
        n = len(poly)
        inside = False
        xinters = 0.0

        p1x, p1y = poly[0].x, poly[0].y
        for i in range(n + 1):
            p2x, p2y = poly[i % n].x, poly[i % n].y
            if point.y > min(p1y, p2y):
                if point.y <= max(p1y, p2y):
                    if point.x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (point.y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or point.x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside
"""


class Collisions:
    def __init__(self) -> None:
        ...

    def objects_collide(self, object1: GameObjectBase, object2: GameObjectBase) -> CollisionDetails:
        if object1.get_collision_type() == CollisionType.NONE or object2.get_collision_type() == CollisionType.NONE:
            toReturn: CollisionDetails = CollisionDetails()
            toReturn.collides = False
            return toReturn

        # Circle to Circle
        if object1.get_collision_type() == CollisionType.CIRCLE and object2.get_collision_type() == CollisionType.CIRCLE:
            point1 = object1.get_position()
            point2 = object2.get_position()
            radiuses: float = object1.get_collision_circle_radius() + object2.get_collision_circle_radius()
            distance: float = math.sqrt(pow(point1.x - point2.x, 2) + pow(point1.y - point2.y, 2))
            if distance < radiuses:
                toReturn: CollisionDetails = CollisionDetails()
                toReturn.collides = True
                toReturn.collision_distance = radiuses - distance

                toReturn.collision_point_object1.x = (point2.x - point1.x) / distance * object1.get_collision_circle_radius() 
                toReturn.collision_point_object1.y = (point2.y - point1.y) / distance * object1.get_collision_circle_radius()

                toReturn.collision_point_object2.x = (point1.x - point2.x) / distance * object2.get_collision_circle_radius()
                toReturn.collision_point_object2.y = (point1.y - point2.y) / distance * object2.get_collision_circle_radius()

                toReturn.reaction_vector_object1.x = (point2.x - point1.x) - toReturn.collision_point_object1.x + toReturn.collision_point_object2.x
                toReturn.reaction_vector_object1.y = (point2.y - point1.y) - toReturn.collision_point_object1.y + toReturn.collision_point_object2.y
                
                toReturn.reaction_vector_object2.x = (point1.x - point2.x) - toReturn.collision_point_object2.x + toReturn.collision_point_object1.x
                toReturn.reaction_vector_object2.y = (point1.y - point2.y) - toReturn.collision_point_object2.y + toReturn.collision_point_object1.y

                return toReturn

            else:
                toReturn: CollisionDetails = CollisionDetails()
                toReturn.collides = False
                return toReturn

        # Poly to Poly
        if object1.get_collision_type() == CollisionType.POLY and object2.get_collision_type() == CollisionType.POLY:

            # if possible we do a stage 1 collision detectionm using radiuses
            point1 = object1.get_position()
            point2 = object2.get_position()
            position_diff = Point2D(point2.x - point1.x, point2.y - point1.y)
            if object1.get_collision_circle_radius() > 0 and object2.get_collision_circle_radius() > 0:
                radiuses: float = object1.get_collision_circle_radius() + object2.get_collision_circle_radius()
                distance: float = math.sqrt(pow(position_diff.x, 2) + pow(position_diff.y, 2))
                if distance > radiuses:
                    toReturn: CollisionDetails = CollisionDetails()
                    toReturn.collides = False
                    return toReturn

            # stage 2 collision detection, using the poly points
            obj1Points: list[Point2D] = object1.get_rotated_collision_poly_points()
            obj1PointsNumber: int = object1.get_no_collision_poly_points()
            obj2Points: list[Point2D] = object2.get_rotated_collision_poly_points()
            obj2PointsNumber: int = object2.get_no_collision_poly_points()

            minColDet: CollisionDetails = CollisionDetails()
            minColDet.collides = False

            # axis of the first object
            for i in range(obj1PointsNumber):
                j = i + 1
                if j == obj1PointsNumber:
                    j = 0

                lineVector: Point2D = Point2D(
                    obj1Points[j].y - obj1Points[i].y,
                    - obj1Points[j].x + obj1Points[i].x 
                    )

                cDet: CollisionDetails = self.collide_on_axis_poly_poly(lineVector= lineVector,
                    obj1Points= obj1Points, obj1PointsNumber= obj1PointsNumber,
                    obj2Points= obj2Points, obj2PointsNumber= obj2PointsNumber,
                    positionDifference= position_diff)

                if not cDet.collides:
                    return cDet
                else:
                    if not minColDet.collides or cDet.collision_distance < minColDet.collision_distance:
                        minColDet = cDet

            # axis of the second object
            for i in range(obj2PointsNumber):
                j = i + 1
                if j == obj2PointsNumber:
                    j = 0

                lineVector: Point2D = Point2D(
                    obj2Points[j].y - obj2Points[i].y,
                    - obj2Points[j].x + obj2Points[i].x 
                    )

                cDet: CollisionDetails = self.collide_on_axis_poly_poly( lineVector= lineVector, 
                    obj1Points= obj1Points, obj1PointsNumber=obj1PointsNumber, 
                    obj2Points= obj2Points, obj2PointsNumber=obj2PointsNumber, 
                    positionDifference=position_diff)
                
                if not cDet.collides:
                    return cDet
                else:
                    if not minColDet.collides or cDet.collision_distance < minColDet.collision_distance:
                        minColDet = cDet

            return minColDet 

        # Poly to Circle
        if object1.get_collision_type() == CollisionType.POLY and object2.get_collision_type() == CollisionType.CIRCLE or \
            object1.get_collision_type() == CollisionType.CIRCLE and object2.get_collision_type() == CollisionType.POLY:

            # if possible we do a stage 1 collision detectionm using radiuses
            point1 = object1.get_position()
            point2 = object2.get_position()
            position_diff = Point2D(point2.x - point1.x, point2.y - point1.y)
            if object1.get_collision_circle_radius() > 0 and object2.get_collision_circle_radius() > 0:
                radiuses: float = object1.get_collision_circle_radius() + object2.get_collision_circle_radius()
                distance: float = math.sqrt(pow(position_diff.x, 2) + pow(position_diff.y, 2))
                if distance > radiuses:
                    toReturn: CollisionDetails = CollisionDetails()
                    toReturn.collides = False
                    return toReturn
            
            # stage 2 collision detection, using the poly points
            swapped: bool = False
            #  Swap them (if necessary) so object1 is always poly and object2 is circle
            if object1.get_collision_type() == CollisionType.CIRCLE and object2.get_collision_type() == CollisionType.POLY:
                swapped = True # Remember if it's swapped so we do the same in the collision details
                object1, object2 = object2, object1

            obj1Points = object1.get_rotated_collision_poly_points()
            obj1PointsNumber = object1.get_no_collision_poly_points()

            point1 = object1.get_position()
            point2 = object2.get_position()
            position_diff = Point2D(point2.x - point1.x, point2.y - point1.y)

            minColDet: CollisionDetails = CollisionDetails()
            minColDet.collision_distance = 0
            minColDet.collides = False

            # axis of the first object (poly)
            closest: Point2D = Point2D(0, 0)
            min_distance: float = math.inf
            for i in range(obj1PointsNumber):
                j = i + 1
                if j == obj1PointsNumber:
                    j = 0

                lineVector: Point2D = Point2D(
                    obj1Points[j].y - obj1Points[i].y,
                    - obj1Points[j].x + obj1Points[i].x 
                    )

                cDet: CollisionDetails = self.collide_on_axis_poly_circle(lineVector= lineVector,
                    obj1Points= obj1Points, obj1PointsNumber= obj1PointsNumber,
                    obj2Radius= object2.get_collision_circle_radius(), positionDifference= position_diff)
                if not cDet.collides:
                    return cDet
                else:
                    if not minColDet.collides or cDet.collision_distance < minColDet.collision_distance:
                        minColDet = cDet

                # closest point on the poly to the circle
                distance: float = math.sqrt(pow(obj1Points[i].x - position_diff.x, 2) + pow(obj1Points[i].y - position_diff.y, 2))
                if distance < min_distance:
                    min_distance = distance
                    closest = obj1Points[i]


            # axis of the second object (circle)
            lineVector: Point2D = Point2D(
                closest.x - position_diff.x, 
                closest.y - position_diff.y)
            cDet: CollisionDetails = self.collide_on_axis_poly_circle(lineVector= lineVector,
                obj1Points= obj1Points, obj1PointsNumber= obj1PointsNumber,
                obj2Radius=object2.get_collision_circle_radius(), positionDifference= position_diff)

            if not cDet.collides:
                return cDet
            else:
                if not minColDet.collides or cDet.collision_distance < minColDet.collision_distance:
                    minColDet = cDet

            # if the objects were swapped, swap them back
            if swapped:
                minColDet.swap_objects()

            return minColDet

        return CollisionDetails()

    def get_projected_point_on_line(self, point: Point2D, line: Point2D) -> Point2D:
        """
        The function takes a point and a line and returns the point on the line that is closest to the
        original point.
        Finds the shadow of the point on the line.
        
        :param point: Point2D = Point2D(0, 0)
        :type point: Point2D
        :param line: Point2D = Point2D(0, 0)
        :type line: Point2D
        :return: A Point2D object
        """
        proj: Point2D = Point2D(0, 0)
        proj.x = ((point.x * line.x + point.y * line.y) / (line.x * line.x + line.y * line.y)) * line.x
        proj.y = ((point.x * line.x + point.y * line.y) / (line.x * line.x + line.y * line.y)) * line.y
        return proj

    def collide_on_axis_poly_poly(self, lineVector: Point2D, 
                                obj1Points: list[Point2D], obj1PointsNumber: int, 
                                obj2Points: list[Point2D], obj2PointsNumber: int, 
                                positionDifference: Point2D) -> CollisionDetails:
        obj1Min: float = math.inf
        obj1MinPoint: int = 999
        obj1Max: float = -math.inf
        obj1MaxPoint: int = 0
        obj2Min: float = math.inf
        obj2MinPoint: int = 999
        obj2Max: float = -math.inf
        obj2MaxPoint: int = 0

        obj1Distances: list[float] = []
        obj2Distances: list[float] = []

        for i in range(obj1PointsNumber):
            projected: Point2D = self.get_projected_point_on_line(obj1Points[i], lineVector)
            distance_on_line: float = math.sqrt(projected.x * projected.x + projected.y * projected.y)
            if projected.x + projected.y < 0:
                distance_on_line = - distance_on_line

            if obj1Min > distance_on_line:
                obj1Min = distance_on_line
                obj1MinPoint = i

            if obj1Max < distance_on_line:
                obj1Max = distance_on_line
                obj1MaxPoint = i

        for i in range(obj2PointsNumber):
            adjustedPoint: Point2D = Point2D(
                obj2Points[i].x + positionDifference.x, 
                obj2Points[i].y + positionDifference.y
                )
            projected: Point2D = self.get_projected_point_on_line(adjustedPoint, lineVector)
            distance_on_line: float = math.sqrt(projected.x * projected.x + projected.y * projected.y)
            if projected.x + projected.y < 0:
                distance_on_line = - distance_on_line

            if obj2Min > distance_on_line:
                obj2Min = distance_on_line
                obj2MinPoint = i

            if obj2Max < distance_on_line:
                obj2Max = distance_on_line
                obj2MaxPoint = i

        toReturn: CollisionDetails = CollisionDetails()

        if obj1Max < obj2Min or obj2Max < obj1Min:
            toReturn.collides = False
        else:
            toReturn.collides = True
            toReturn.collision_distance = min(abs(obj1Max - obj2Min), abs(obj1Min - obj2Max))
            toReturn.collision_point_object1.x = 0
            toReturn.collision_point_object1.y = 0
            toReturn.collision_point_object2.x = 0
            toReturn.collision_point_object2.y = 0

            vectorLenght: float = math.sqrt(lineVector.x * lineVector.x + lineVector.y * lineVector.y)

            if abs(obj1Max - obj2Min) < abs(obj1Min - obj2Max):
                minDistanceToOtherObject = math.inf
                noObj1LinePoints: int = 0
                closestObj1Point: Point2D = Point2D(0, 0)

                for i in range(obj1PointsNumber):
                    if abs(obj1Distances[i] - obj1Distances[obj1MaxPoint]) < 0.01:
                        distanceToOtherObject = math.sqrt(pow(obj1Points[i].x - positionDifference.x, 2) + pow(obj1Points[i].y - positionDifference.y, 2))
                        if minDistanceToOtherObject > distanceToOtherObject:
                            minDistanceToOtherObject = distanceToOtherObject
                            closestObj1Point = obj1Points[i]
                        noObj1LinePoints += 1

                minDistanceToOtherObject = math.inf
                noObj2LinePoints: int = 0
                closestObj2Point: Point2D
                for i in range(obj2PointsNumber):
                    if abs(obj2Distances[i] - obj2Distances[obj2MinPoint]) < 0.01:
                        distanceToOtherObject = math.sqrt(pow(obj2Points[i].x - positionDifference.x, 2) + pow(obj2Points[i].y - positionDifference.y, 2))
                        if minDistanceToOtherObject > distanceToOtherObject:
                            minDistanceToOtherObject = distanceToOtherObject
                            closestObj2Point = obj2Points[i]
                        noObj2LinePoints += 1

                if noObj1LinePoints == 1 and noObj2LinePoints > 1:
                    toReturn.collision_point_object1.x = obj1Points[obj1MaxPoint].x
                    toReturn.collision_point_object1.y = obj1Points[obj1MaxPoint].y
                    toReturn.reaction_vector_object1.x = lineVector.x / vectorLenght * toReturn.collision_distance
                    toReturn.reaction_vector_object1.y = lineVector.y / vectorLenght * toReturn.collision_distance
                    if self.dot_product(toReturn.reaction_vector_object1, toReturn.collision_point_object1) > 0:
                        toReturn.reaction_vector_object1.x = -toReturn.reaction_vector_object1.x
                        toReturn.reaction_vector_object1.y = -toReturn.reaction_vector_object1.y

                    toReturn.collision_point_object2.x = toReturn.collision_point_object1.x - positionDifference.x + toReturn.reaction_vector_object1.x
                    toReturn.collision_point_object2.y = toReturn.collision_point_object1.y - positionDifference.y + toReturn.reaction_vector_object1.y
                    toReturn.reaction_vector_object2.x = -toReturn.reaction_vector_object1.x
                    toReturn.reaction_vector_object2.y = -toReturn.reaction_vector_object1.y

                if noObj1LinePoints > 1 and noObj2LinePoints == 1:
                    toReturn.collision_point_object2.x = obj2Points[obj2MinPoint].x
                    toReturn.collision_point_object2.y = obj2Points[obj2MinPoint].y
                    toReturn.reaction_vector_object2.x = lineVector.x / vectorLenght * toReturn.collision_distance
                    toReturn.reaction_vector_object2.y = lineVector.y / vectorLenght * toReturn.collision_distance
                    if self.dot_product(toReturn.reaction_vector_object2, toReturn.collision_point_object2) > 0:
                        toReturn.reaction_vector_object2.x = -toReturn.reaction_vector_object2.x
                        toReturn.reaction_vector_object2.y = -toReturn.reaction_vector_object2.y

                    toReturn.collision_point_object1.x = toReturn.collision_point_object2.x + positionDifference.x + toReturn.reaction_vector_object2.x
                    toReturn.collision_point_object1.y = toReturn.collision_point_object2.y + positionDifference.y + toReturn.reaction_vector_object2.y
                    toReturn.reaction_vector_object1.x = -toReturn.reaction_vector_object2.x
                    toReturn.reaction_vector_object1.y = -toReturn.reaction_vector_object2.y

                if noObj1LinePoints > 1 and noObj2LinePoints > 1:
                    toReturn.collision_point_object1.x = closestObj1Point.x
                    toReturn.collision_point_object1.y = closestObj1Point.y
                    toReturn.reaction_vector_object1.x = lineVector.x / vectorLenght * toReturn.collision_distance
                    toReturn.reaction_vector_object1.y = lineVector.y / vectorLenght * toReturn.collision_distance

                    if self.dot_product(toReturn.reaction_vector_object1, toReturn.collision_point_object1) > 0:
                        toReturn.reaction_vector_object1.x = -toReturn.reaction_vector_object1.x
                        toReturn.reaction_vector_object1.y = -toReturn.reaction_vector_object1.y

                    toReturn.collision_point_object2.x = closestObj1Point.x
                    toReturn.collision_point_object2.y = closestObj1Point.y
                    toReturn.reaction_vector_object2.x = lineVector.x / vectorLenght * toReturn.collision_distance
                    toReturn.reaction_vector_object2.y = lineVector.y / vectorLenght * toReturn.collision_distance

                    if self.dot_product(toReturn.reaction_vector_object2, toReturn.collision_point_object2) > 0:
                        toReturn.reaction_vector_object2.x = -toReturn.reaction_vector_object2.x
                        toReturn.reaction_vector_object2.y = -toReturn.reaction_vector_object2.y

            else:
                minDistanceToOtherObject: float = math.inf
                noObj1LinePoints: int = 0
                closestObj1Point: Point2D = Point2D(0, 0)
                for i in range(obj1PointsNumber):
                    if abs(obj1Distances[i] - obj1Distances[obj1MinPoint]) < 0.01:
                        distanceToOtherObject: float = math.sqrt(pow(obj1Points[i].x - positionDifference.x, 2) + pow(obj1Points[i].y - positionDifference.y, 2))
                        if minDistanceToOtherObject > distanceToOtherObject:
                            minDistanceToOtherObject = distanceToOtherObject
                            closestObj1Point = obj1Points[i]
                        noObj1LinePoints += 1

                minDistanceToOtherObject = math.inf
                noObj2LinePoints: int = 0
                closestObj2Point: Point2D = Point2D(0, 0)
                for i in range(obj2PointsNumber):
                    if abs(obj2Distances[i] - obj2Distances[obj2MinPoint]) < 0.01:
                        distanceToOtherObject = math.sqrt(pow(obj2Points[i].x - positionDifference.x, 2) + pow(obj2Points[i].y - positionDifference.y, 2))
                        if minDistanceToOtherObject > distanceToOtherObject:
                            minDistanceToOtherObject = distanceToOtherObject
                            closestObj2Point = obj2Points[i]
                        noObj2LinePoints += 1

                if noObj1LinePoints == 1 and noObj2LinePoints > 1:
                    toReturn.collision_point_object1.x = obj1Points[obj1MinPoint].x
                    toReturn.collision_point_object1.y = obj1Points[obj1MinPoint].y
                    toReturn.reaction_vector_object1.x = lineVector.x / vectorLenght * toReturn.collision_distance
                    toReturn.reaction_vector_object1.y = lineVector.y / vectorLenght * toReturn.collision_distance
                    if self.dot_product(toReturn.reaction_vector_object1, toReturn.collision_point_object1) > 0:
                        toReturn.reaction_vector_object1.x = -toReturn.reaction_vector_object1.x
                        toReturn.reaction_vector_object1.y = -toReturn.reaction_vector_object1.y

                    toReturn.collision_point_object2.x = toReturn.collision_point_object1.x - positionDifference.x + toReturn.reaction_vector_object1.x
                    toReturn.collision_point_object2.y = toReturn.collision_point_object1.y - positionDifference.y + toReturn.reaction_vector_object1.y
                    toReturn.reaction_vector_object2.x = -toReturn.reaction_vector_object1.x
                    toReturn.reaction_vector_object2.y = -toReturn.reaction_vector_object1.y

                if noObj1LinePoints > 1 and noObj2LinePoints == 1:
                    toReturn.collision_point_object2.x = obj2Points[obj2MinPoint].x
                    toReturn.collision_point_object2.y = obj2Points[obj2MinPoint].y
                    toReturn.reaction_vector_object2.x = lineVector.x / vectorLenght * toReturn.collision_distance
                    toReturn.reaction_vector_object2.y = lineVector.y / vectorLenght * toReturn.collision_distance
                    if self.dot_product(toReturn.reaction_vector_object2, toReturn.collision_point_object2) > 0:
                        toReturn.reaction_vector_object2.x = -toReturn.reaction_vector_object2.x
                        toReturn.reaction_vector_object2.y = -toReturn.reaction_vector_object2.y

                    toReturn.collision_point_object1.x = toReturn.collision_point_object2.x + positionDifference.x + toReturn.reaction_vector_object2.x
                    toReturn.collision_point_object1.y = toReturn.collision_point_object2.y + positionDifference.y + toReturn.reaction_vector_object2.y
                    toReturn.reaction_vector_object1.x = -toReturn.reaction_vector_object2.x
                    toReturn.reaction_vector_object1.y = -toReturn.reaction_vector_object2.y

                if noObj1LinePoints == 1 and noObj2LinePoints == 1:
                    toReturn.collision_point_object1.x = obj1Points[obj1MinPoint].x
                    toReturn.collision_point_object1.y = obj1Points[obj1MinPoint].y
                    toReturn.reaction_vector_object1.x = lineVector.x / vectorLenght * toReturn.collision_distance
                    toReturn.reaction_vector_object1.y = lineVector.y / vectorLenght * toReturn.collision_distance
                    if self.dot_product(toReturn.reaction_vector_object1, toReturn.collision_point_object1) > 0:
                        toReturn.reaction_vector_object1.x = -toReturn.reaction_vector_object1.x
                        toReturn.reaction_vector_object1.y = -toReturn.reaction_vector_object1.y

                    toReturn.collision_point_object2.x = obj2Points[obj2MinPoint].x
                    toReturn.collision_point_object2.y = obj2Points[obj2MinPoint].y
                    toReturn.reaction_vector_object2.x = lineVector.x / vectorLenght * toReturn.collision_distance
                    toReturn.reaction_vector_object2.y = lineVector.y / vectorLenght * toReturn.collision_distance
                    if self.dot_product(toReturn.reaction_vector_object2, toReturn.collision_point_object2) > 0:
                        toReturn.reaction_vector_object2.x = -toReturn.reaction_vector_object2.x
                        toReturn.reaction_vector_object2.y = -toReturn.reaction_vector_object2.y

        return toReturn

    def collide_on_axis_poly_circle(self, lineVector: Point2D, 
                                    obj1Points: list[Point2D], obj1PointsNumber: int, 
                                    obj2Radius: float, positionDifference: Point2D) -> CollisionDetails:
        points_iter = iter(obj1Points) 
        
        obj1Min: float = math.inf
        obj1Max: float = -math.inf
        obj2Min: float = math.inf
        obj2Max: float = -math.inf

        for i in range(obj1PointsNumber):
            projected: Point2D = self.get_projected_point_on_line(obj1Points[i], lineVector)
            distance_on_line: float = math.sqrt(projected.x * projected.x + projected.y * projected.y)
            if projected.x + projected.y < 0:
                distance_on_line = - distance_on_line

            if obj1Min > distance_on_line:
                obj1Min = distance_on_line

            if obj1Max < distance_on_line:
                obj1Max = distance_on_line

        projecteds: Point2D = self.get_projected_point_on_line(positionDifference, lineVector)
        distance_on_line: float = math.sqrt(projecteds.x * projecteds.x + projecteds.y * projecteds.y)
        if projecteds.x + projecteds.y < 0:
            distance_on_line = - distance_on_line
        obj2Min = distance_on_line - obj2Radius
        obj2Max = distance_on_line + obj2Radius

        if obj1Max < obj2Min or obj2Max < obj1Min:
            toReturn = CollisionDetails()
            toReturn.collides = False
            return toReturn

        vectorLenght: float = math.sqrt(lineVector.x * lineVector.x + lineVector.y * lineVector.y)
        collX: float = lineVector.x / vectorLenght * obj2Radius 
        collY: float = lineVector.y / vectorLenght * obj2Radius
        if self.dot_product(positionDifference, Point2D(collX, collY)) > 0:
            collX = -collX
            collY = -collY

        toReturn = CollisionDetails()
        toReturn.collides = True
        toReturn.collision_distance = min(abs(obj1Max - obj2Min), abs(obj1Min - obj2Max))

        toReturn.collision_point_object2.x = collX
        toReturn.collision_point_object2.y = collY
        toReturn.reaction_vector_object2.x = lineVector.x / vectorLenght * toReturn.collision_distance
        toReturn.reaction_vector_object2.y = lineVector.y / vectorLenght * toReturn.collision_distance
        if self.dot_product(toReturn.reaction_vector_object2, toReturn.collision_point_object2) > 0:
            toReturn.reaction_vector_object2.x = -toReturn.reaction_vector_object2.x
            toReturn.reaction_vector_object2.y = -toReturn.reaction_vector_object2.y

        toReturn.collision_point_object1.x = collX + positionDifference.x + toReturn.reaction_vector_object2.x
        toReturn.collision_point_object1.y = collY + positionDifference.y + toReturn.reaction_vector_object2.y
        toReturn.reaction_vector_object1.x = -toReturn.reaction_vector_object2.x
        toReturn.reaction_vector_object1.y = -toReturn.reaction_vector_object2.y

        return toReturn

    def dot_product(self, point1: Point2D, point2: Point2D) -> float:
        return point1.x * point2.x + point1.y * point2.y


class CollisionDetails:
    def __init__(self):
        self.collides: bool
        self.collision_distance: float
        self.collision_point_object1: Point2D
        self.collision_point_object2: Point2D
        self.reaction_vector_object1: Point2D
        self.reaction_vector_object2: Point2D

    def swap_objects(self):
        aux: float

        aux = self.collision_point_object1.x
        self.collision_point_object1.x = self.collision_point_object2.x
        self.collision_point_object2.x = aux
        aux = self.collision_point_object1.y
        self.collision_point_object1.y = self.collision_point_object2.y
        self.collision_point_object2.y = aux

        aux = self.reaction_vector_object1.x
        self.reaction_vector_object1.x = self.reaction_vector_object2.x
        self.reaction_vector_object2.x = aux
        aux = self.reaction_vector_object1.y
        self.reaction_vector_object1.y = self.reaction_vector_object2.y
        self.reaction_vector_object2.y = aux


class ParticleSystem:
    def __init__(self):
        self.particles: list[Particle] = []
        self.numberOfParticles: int
        self.maxNumberOfParticles: int
        self.timeSinceLastEmission: float = 0.0

        self.particleSpeed: Point2D
        self.particleLifetime: float

    def logic(self, deltaTime: float):
        for particle in self.particles:
            particle.logic(deltaTime)
            particle.GrowOld(deltaTime)

        for i, particle in sorted(enumerate(self.particles), reverse=True):
            if particle.IsOld():
                self.particles.pop(i)

        self.timeSinceLastEmission += deltaTime
        if self.timeSinceLastEmission > self.particleLifetime / self.maxNumberOfParticles:
            self.timeSinceLastEmission = 0.0
            self.particles[self.numberOfParticles].EmitParticle()
            self.numberOfParticles += 1

        self.particles = [particle for particle in self.particles if not particle.IsOld()]
        self.numberOfParticles = len(self.particles)

    def draw(self):
        for particle in self.particles:
            particle.draw()

    def EmitParticle(self, deltaTime: float):
        ...


class Particle:
    def __init__(self):
        self.age: float = 0.0
        self.particleLifetime: float = 0.0

    def EmitParticle(self):
        ...

    def GrowOld(self, deltaTime: float):
        self.age += deltaTime

    def IsOld(self) -> bool:
        return self.age > self.particleLifetime

    def GetAge(self) -> float:
        return self.age

    def logic(self, deltaTime: float):
        ...

    def draw(self):
        ...


class Fire(Particle):
    def __init__(self, pos: Point2D, spreadSize: int):
        self.position: Point2D = pos
        self.spread: int = spreadSize
        self.particleLifetime: float = FIRE_PARTICLE_LIFETIME
        self.maxNumberOfParticles: int = 1000

    def EmitParticle(self):
        newPosition: Point2D = Point2D(0, 0)
        newPosition.x = self.position.x + random.randint(1, self.spread * 2) - self.spread
        newPosition.y = self.position.y

        newSpeed: Point2D = Point2D(0, 0)
        newSpeed.x = 0
        newSpeed.y = -100 - random.randint(1, 30)

        newParticle: FireParticle = FireParticle(newPosition, newSpeed)
        return newParticle


class FireParticle(Particle):
    def __init__(self, pos: Point2D, speed: Point2D):
        self.position: Point2D = pos
        self.speed: Point2D = speed
        self.particleLifetime: float = FIRE_PARTICLE_LIFETIME

        self.sidewaysMovement: float = random.randrange(0, 40)
        self.sidewaysMovementSpeed: float = random.randrange(0, 40)

    def logic(self, deltaTime: float):
        self.position.x += self.speed.x * deltaTime
        self.position.y += self.speed.y * deltaTime

    def draw(self):
        ...

    def IsOld(self) -> bool:
        return super().IsOld()


class Rain(Particle):
    def __init__(self, pos: Point2D):
        self.position: Point2D = pos
        self.maxNumberOfParticles: int = 5000
        self.particleLifetime: float = RAIN_PARTICLE_LIFETIME

    def EmitParticle(self) -> RainParticle:
        newPosition: Point2D = Point2D(0, 0)
        newPosition.x = random.randint(0, SCREEN_WIDTH)
        newPosition.y = self.position.y

        newSpeed: Point2D = Point2D(0, 0)
        newSpeed.x = random.randint(1, 40) - 20
        newSpeed.y = 500 - random.randint(1, 300)

        newParticle: RainParticle = RainParticle(newPosition, newSpeed)
        return newParticle


class RainParticle(Particle):
    def __init__(self, pos: Point2D, speed: Point2D):
        self.position: Point2D = pos
        self.speed: Point2D = speed
        self.particleLifetime: float = RAIN_PARTICLE_LIFETIME

    def logic(self, deltaTime: float):
        self.position.x += self.speed.x * deltaTime
        self.position.y += self.speed.y * deltaTime

    def draw(self):
        ...

    def IsOld(self) -> bool:
        return super().IsOld()


class Explosion(Particle):
    def __init__(self, pos: Point2D, spreadSize: int):
        self.position: Point2D = pos
        self.spread: int = spreadSize
        self.maxNumberOfParticles: int = 1000
        self.particleLifetime: float = EXPLOSION_PARTICLE_LIFETIME

        self.particleSpeed: Point2D = Point2D(0, 0)
        self.timeSinceLastEmission: float = 0.0
        self.particles: list[ExplosionParticle] = []

    def EmitParticle(self) -> ExplosionParticle:
        newPosition: Point2D = Point2D(0, 0)
        newPosition.x = self.position.x + random.randint(1, self.spread * 2) - self.spread
        newPosition.y = self.position.y + random.randint(1, self.spread * 2) - self.spread

        newSpeed: Point2D = Point2D(0, 0)
        newSpeed.x = random.randint(1, 40) - 20
        newSpeed.y = random.randint(1, 40) - 20

        newParticle: ExplosionParticle = ExplosionParticle(newPosition, newSpeed)
        return newParticle


class ExplosionParticle(Particle):
    def __init__(self, pos: Point2D, speed: Point2D):
        self.position: Point2D = pos
        self.speed: Point2D = speed
        self.particleLifetime: float = EXPLOSION_PARTICLE_LIFETIME

    def logic(self, deltaTime: float):
        self.position.x += self.speed.x * deltaTime
        self.position.y += self.speed.y * deltaTime

    def draw(self):
        ...

    def IsOld(self) -> bool:
        return super().IsOld()


class Smoke(Particle):
    def __init__(self, pos: Point2D, spreadSize: int):
        self.position: Point2D = pos
        self.spread: int = spreadSize
        self.maxNumberOfParticles: int = 1000
        self.particleLifetime: float = SMOKE_PARTICLE_LIFETIME

        self.particleSpeed: Point2D = Point2D(0, 0)
        self.timeSinceLastEmission: float = 0.0
        self.particles: list[SmokeParticle] = []

    def EmitParticle(self) -> SmokeParticle:
        newPosition: Point2D = Point2D(0, 0)
        newPosition.x = self.position.x + random.randint(1, self.spread * 2) - self.spread
        newPosition.y = self.position.y + random.randint(1, self.spread * 2) - self.spread

        newSpeed: Point2D = Point2D(0, 0)
        newSpeed.x = random.randint(1, 40) - 20
        newSpeed.y = random.randint(1, 40) - 20

        newParticle: SmokeParticle = SmokeParticle(newPosition, newSpeed)
        return newParticle


class SmokeParticle(Particle):
    def __init__(self, pos: Point2D, speed: Point2D):
        self.position: Point2D = pos
        self.speed: Point2D = speed
        self.particleLifetime: float = SMOKE_PARTICLE_LIFETIME

    def logic(self, deltaTime: float):
        self.position.x += self.speed.x * deltaTime
        self.position.y += self.speed.y * deltaTime

    def draw(self):
        ...

    def IsOld(self) -> bool:
        return super().IsOld()

# ClassNames
# MethodNames
# variableName
# CONSTANT_NAME
# function_name