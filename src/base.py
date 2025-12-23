from typing import Optional
from math import sqrt

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({round(self.x, 2)}, {round(self.y, 2)})"

    def __eq__(self, other):
        if not isinstance(other, Point): return False
        return abs(self.x - other.x) < 1e-4 and abs(self.y - other.y) < 1e-4

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def is_on_segment(self, a: 'Point', b: 'Point') -> bool:
        cross_product = (self.y - a.y) * (b.x - a.x) - (self.x - a.x) * (b.y - a.y)
        if abs(cross_product) > 1e-4:
            return False
        min_x, max_x = min(a.x, b.x) - 1e-4, max(a.x, b.x) + 1e-4
        min_y, max_y = min(a.y, b.y) - 1e-4, max(a.y, b.y) + 1e-4
        return min_x <= self.x <= max_x and min_y <= self.y <= max_y

class Vector:
    @staticmethod
    def get_unit_normal(p1: Point, p2: Point) -> Point:
        dx, dy = p2.x - p1.x, p2.y - p1.y
        length = sqrt(dx**2 + dy**2)
        if length < 1e-9:
            return Point(0, 0)
        return Point(-dy / length, dx / length)

class Line:
    def __init__(self, a: float, b: float, c: float):
        self.a, self.b, self.c = a, b, c

    @classmethod
    def from_offset_edge(cls, p1: Point, p2: Point, d: float) -> 'Line':
        n = Vector.get_unit_normal(p1, p2)
        new_p1 = p1 + (n * d)
        new_p2 = p2 + (n * d)

        a = new_p1.y - new_p2.y
        b = new_p2.x - new_p1.x
        c = a * new_p1.x + b * new_p1.y
        return cls(a, b, c)

    @classmethod
    def from_points(cls, p1: Point, p2: Point) -> 'Line':
        a = p1.y - p2.y
        b = p2.x - p1.x
        c = a * p1.x + b * p1.y
        return cls(a, b, c)

    def intersect(self, other: 'Line') -> Optional[Point]:
        det = self.a * other.b - other.a * self.b
        if abs(det) < 1e-9:
            return None
        det_x = self.c * other.b - self.b * other.c
        det_y = self.a * other.c - self.c * other.a
        return Point(det_x / det, det_y / det)
