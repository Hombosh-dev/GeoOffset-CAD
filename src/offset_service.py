from typing import List
from polygon import Polygon, Point


class CADOffsetService:
    def __init__(self, strategy):
        self.strategy = strategy

    def offset_polygon(self, coords: List[tuple], d: float) -> List[Polygon]:
        vertices = [Point(x, y) for x, y in coords]
        poly = Polygon(vertices)
        return self.strategy.apply(poly, d)
