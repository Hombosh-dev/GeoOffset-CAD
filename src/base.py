from typing import Optional
from math import sqrt

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({round(self.x, 2)}, {round(self.y, 2)})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

class Vector:
    @staticmethod
    def get_unit_normal(p1: Point, p2: Point) -> Point:
        dx = p2.x - p1.x
        dy = p2.y - p1.y

        length = sqrt(dx**2 + dy**2)

        return Point(-dy / length, dx / length)

class Line:
    """
    Line: Ax + By = C
    """
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def from_offset_edge(cls, p1: Point, p2: Point, d: float) -> 'Line':
        n = Vector.get_unit_normal(p1, p2)
        new_p1 = p1 + (n * d)
        new_p2 = p1 + (n * d)

        a = new_p1.y - new_p2.y
        b = new_p2.x - new_p1.x
        c = a * new_p1.x + b * new_p1.y
        return cls(a,b,c)


    def intersect(self, other: 'Line') -> Optional[Point] | None:
        det = self.a * other.b - other.a * self.b
        if int(det) == 0:
            return None
        det_x = self.c * other.b - self.b * other.c
        det_y = self.a * other.c - self.c * other.a

        return Point(det_x/det, det_y/det)
