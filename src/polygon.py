from typing import List
from base import Point, Line

class Polygon:
    def __init__(self, vertices: List[Point]):
        self.vertices = vertices

    # Gauss formula
    def area(self) -> float:
        n = len(self.vertices)
        if n < 3: return 0.0
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.vertices[i].x * self.vertices[j].y
            area -= self.vertices[j].x * self.vertices[i].y
        return abs(area) / 2.0

    def is_clockwise(self) -> bool:
        n = len(self.vertices)
        signed_area = 0.0
        for i in range(n):
            j = (i + 1) % n
            signed_area += (self.vertices[i].x * self.vertices[j].y)
            signed_area -= (self.vertices[j].x * self.vertices[i].y)
        return signed_area < 0
