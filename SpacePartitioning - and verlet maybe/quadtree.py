import math
import pygame
from typing import Any


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
    def __init__(self, boundary: Rectangle, capacity: int, depth: int = 0):

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
            self.North_East.insert(point) 
            self.North_West.insert(point) 
            self.South_East.insert(point) 
            self.South_West.insert(point) 

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