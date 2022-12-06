import math
import time
import pygame
from typing import Any
import json 


class Point:
    def __init__(self, x: int, y: int, userData: Any) -> None:
        self.x = x
        self.y = y
        self.userData = userData

    # skips the math.sqrt() call for performance
    def sqDistanceFrom(self, other: "Point") -> float:
        dx = other.x - self.x
        dy = other.y - self.y

        return dx * dx + dy * dy

    def distanceFrom(self, other: "Point") -> float:
        return math.sqrt(self.sqDistanceFrom(other))


class Rectangle:
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point: Point) -> bool:
        return (
            self.x <= point.x <= self.x + self.w and
            self.y <= point.y <= self.y + self.h
        )

    def intersects(self, range: "Rectangle") -> bool:
        return not (
            self.x > range.x + range.w or
            self.x + self.w < range.x or
            self.y > range.y + range.h or
            self.y + self.h < range.y
        )

    def subdivide(self, quadrant: str) -> "Rectangle":
        if quadrant == "nw":
            x, y = self.x, self.y
            w, h = int(self.w / 2), int(self.h / 2)
            return Rectangle(x, y, w, h)
        elif quadrant == "ne":
            x, y = int(self.x + self.w / 2), self.y
            w, h = int(self.w / 2), int(self.h / 2)
            return Rectangle(x, y, w, h)
        elif quadrant == "sw":
            x, y = self.x, int(self.y + self.h / 2)
            w, h = int(self.w / 2), int(self.h / 2)
            return Rectangle(x, y, w, h)
        elif quadrant == "se":
            x, y = int(self.x + self.w / 2), int(self.y + self.h / 2)
            w, h = int(self.w / 2), int(self.h / 2)
            return Rectangle(x, y, w, h)
        else:
            raise ValueError("quadrant must be one of 'nw', 'ne', 'sw', 'se'")

    def xDistanceFrom(self, point: Point) -> int:
        if self.x <= point.x <= self.x + self.w:
            return 0

        return min(abs(point.x - self.x), abs(point.x - self.x + self.w)) # type: ignore

    def yDistanceFrom(self, point: Point) -> int:
        if self.y <= point.y <= self.y + self.h:
            return 0

        return min(abs(point.y - self.y), abs(point.y - self.y + self.h))

    def distanceFrom(self, point: Point) -> float:
        dx = self.xDistanceFrom(point)
        dy = self.yDistanceFrom(point)

        return math.sqrt(dx * dx + dy * dy)

    def sqDistanceFrom(self, point: Point) -> float:
        dx = self.xDistanceFrom(point)
        dy = self.yDistanceFrom(point)

        return dx * dx + dy * dy


class Circle:
    def __init__(self, x: int, y: int, r: int) -> None:
        self.x = x
        self.y = y
        self.r = r

        self.rSquared = r * r

    def contains(self, point: Point) -> bool:
        d = math.pow(point.x - self.x, 2) + math.pow(point.y - self.y, 2)
        return d <= self.rSquared

    def intersects(self, range: Rectangle) -> bool:
        xDist = abs(range.x - self.x)
        yDist = abs(range.y - self.y)

        r = self.r

        w = range.w # / 2
        h = range.h # / 2

        """edges = [
            math.pow(xDist - w, 2) + math.pow(yDist - h, 2),
            math.pow(xDist - w, 2) + math.pow(yDist, 2),
            math.pow(xDist, 2) + math.pow(yDist - h, 2),
            math.pow(xDist, 2) + math.pow(yDist, 2)
        ]
        closest_edge = min(edges)"""

        # no intersection
        if xDist > (r + w) or yDist > (r + h):
            return False

        # intersection within the circle
        if xDist <= w or yDist <= h:
            return True

        # intersection on the edge of the circle
        # print(closest_edge, r ** 2)
        return True # closest_edge <= self.rSquared 


class QuadTree:
    def __init__(self, boundary: Circle | Rectangle, capacity: int, depth: int = 0):
        if not boundary:
            raise Exception('boundary is required')

        if not isinstance(boundary, Rectangle):
            raise TypeError('boundary must be a Rectangle')

        if not isinstance(capacity, int):
            raise TypeError('capacity must be an integer')

        if capacity < 1:
            raise ValueError('capacity must be greater than 0')

        self.boundary = boundary
        self.capacity = capacity
        self.points: list[Point] = []
        self.divided: bool = False

        self.depth = depth
        self.MAX_DEPTH: int = 8

        self.North_East: QuadTree 
        self.North_West: QuadTree
        self.South_East: QuadTree 
        self.South_West: QuadTree 

    def get_childern(self):
        if self.divided:
            return [self.North_East, self.North_West, self.South_East, self.South_West]
        return []

    def clear(self):
        self.points = []

        if self.divided:
            self.divided = False
            del self.North_West
            del self.North_East
            del self.South_West
            del self.South_East

    @staticmethod 
    def create():
        return QuadTree(Rectangle(0, 0, 800, 800), 4)

    def toJSON(self) -> dict:
        obj = {}

        if self.divided:
            if self.North_East.divided or len(self.North_East.points) > 0:
                obj['ne'] = self.North_East.toJSON()
            if self.North_West.divided or len(self.North_West.points) > 0:
                obj['nw'] = self.North_West.toJSON()
            if self.South_East.divided or len(self.South_East.points) > 0:
                obj['se'] = self.South_East.toJSON()
            if self.South_West.divided or len(self.South_West.points) > 0:
                obj['sw'] = self.South_West.toJSON()
        else:
            obj['points'] = self.points

        
        if self.depth == 0:
            obj['capacity'] = self.capacity
            obj['x'] = self.boundary.x
            obj['y'] = self.boundary.y
            obj['w'] = self.boundary.w
            obj['h'] = self.boundary.h

        return obj

    @staticmethod #
    def fromJSON(obj: dict) -> "QuadTree":
        if 'x' not in obj or 'y' not in obj or 'w' not in obj or 'h' not in obj:
            raise Exception('invalid json')

        boundary = Rectangle(obj['x'], obj['y'], obj['w'], obj['h'])
        capacity = obj['capacity'] if 'capacity' in obj else 4
        tree = QuadTree(boundary, capacity)

        if 'points' in obj:
            for point in obj['points']:
                tree.insert(point)

        if 'ne' in obj:
            tree.North_East = QuadTree.fromJSON(obj['ne'])
            tree.North_East.depth = tree.depth + 1
            tree.divided = True
        if 'nw' in obj:
            tree.North_West = QuadTree.fromJSON(obj['nw'])
            tree.North_West.depth = tree.depth + 1
            tree.divided = True
        if 'se' in obj:
            tree.South_East = QuadTree.fromJSON(obj['se'])
            tree.South_East.depth = tree.depth + 1
            tree.divided = True
        if 'sw' in obj:
            tree.South_West = QuadTree.fromJSON(obj['sw'])
            tree.South_West.depth = tree.depth + 1
            tree.divided = True

        return tree

    def subdivide(self) -> None:
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        ne = Rectangle(int(x + w / 2), y, int(w / 2), int(h / 2))
        self.North_East = QuadTree(ne, self.capacity)
        self.North_East.depth = self.depth + 1
        self.North_East.MAX_DEPTH = self.MAX_DEPTH

        nw = Rectangle(x, y, int(w / 2), int(h / 2))
        self.North_West = QuadTree(nw, self.capacity)
        self.North_West.depth = self.depth + 1
        self.North_West.MAX_DEPTH = self.MAX_DEPTH

        se = Rectangle(int(x + w / 2), int(y + h / 2), int(w / 2), int(h / 2))
        self.South_East = QuadTree(se, self.capacity)
        self.South_East.depth = self.depth + 1
        self.South_East.MAX_DEPTH = self.MAX_DEPTH

        sw = Rectangle(x, int(y + h / 2), int(w / 2), int(h / 2))
        self.South_West = QuadTree(sw, self.capacity)
        self.South_West.depth = self.depth + 1
        self.South_West.MAX_DEPTH = self.MAX_DEPTH

        self.divided: bool = True

        # Move points to their appropriate child
        for point in self.points:
            inserted = \
            self.North_East.insert(point) or \
            self.North_West.insert(point) or \
            self.South_East.insert(point) or \
            self.South_West.insert(point) 

            """if not inserted:
                print(point.x, point.y, point.userData)
                pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), (point.x, point.y), 20, 2)
                pygame.display.update()
                time.sleep(3)
                raise Exception(f'Point {point} from {self.points=} was not inserted in any of: \n \
                {self.North_East.boundary=}, {self.North_East.points=} \n \
                {self.North_West.boundary=}, {self.North_West.points=} \n \
                {self.South_East.boundary=}, {self.South_East.points=} \n \
                {self.South_West.boundary=}, {self.South_West.points=} \n \
                while trying to move out of boundary {self.boundary=}'
                )"""

        self.points = []

    def insert(self, point: Point) -> bool:
        if not self.boundary.contains(point):
            return False

        if not self.divided:
            if len(self.points) < self.capacity or self.depth == self.MAX_DEPTH:
                self.points.append(point)
                return True

            self.subdivide()
        
        return self.North_East.insert(point) or \
                self.North_West.insert(point) or \
                self.South_East.insert(point) or \
                self.South_West.insert(point)

    def query(self, range: Circle, found: list[Point]) -> list[Point]:
        if not range.intersects(self.boundary):
            return found

        if self.divided:
            self.North_East.query(range, found)
            self.North_West.query(range, found)
            self.South_East.query(range, found)
            self.South_West.query(range, found)
            return found

        for point in self.points:
            if range.contains(point):
                found.append(point)

        return found

    def deleteInRange(self, range: Circle | Rectangle) -> None:
        if self.divided:
            self.North_East.deleteInRange(range)
            self.North_West.deleteInRange(range)
            self.South_East.deleteInRange(range)
            self.South_West.deleteInRange(range)

        # delete points witch range contains
        self.points = [point for point in self.points if not range.contains(point)]

    def show(self, surface: pygame.surface.Surface, color: tuple[int, int, int] = (255, 255, 255)) -> None: 
        pygame.draw.rect(surface, color, [self.boundary.x, self.boundary.y, self.boundary.w, self.boundary.h], 1)

        if self.divided:
            self.North_East.show(surface, color)
            self.North_West.show(surface, color)
            self.South_East.show(surface, color)
            self.South_West.show(surface, color)