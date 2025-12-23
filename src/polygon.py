from typing import List
from base import Point, Line

class Polygon:
    def __init__(self, vertices: List[Point]):
        self.vertices = vertices

    # Gauss formula
    def area(self) -> float:
        n = len(self.vertices)
        if n < 3:
            return 0.0
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

class MiterOffsetStrategy():
    def apply(self, polygon: Polygon, d: float) -> List[Polygon]:
        if abs(d) < 1e-9:
            return [polygon]

        original_is_cw = polygon.is_clockwise()
        original_area = polygon.area()
        actual_d = d if original_is_cw else -d
        vertices = polygon.vertices
        n = len(vertices)
        new_points = []

        for i in range(n):
            p_prev = vertices[(i - 1) % n]
            p_curr = vertices[i]
            p_next = vertices[(i + 1) % n]

            l1 = Line.from_offset_edge(p_prev, p_curr, actual_d)
            l2 = Line.from_offset_edge(p_curr, p_next, actual_d)
            p_int = l1.intersect(l2)
            if p_int:
                new_points.append(p_int)

        points_with_nodes = self._inject_intersections(new_points)
        candidate_polys = self._process_points(points_with_nodes)
        valid_polys = []
        for p in candidate_polys:
            if p.area() < 1e-4:
                continue
            if d < 0:
                if p.is_clockwise() != original_is_cw:
                    continue
                if p.area() > original_area:
                    continue
            valid_polys.append(p)

        return valid_polys

    # Logic for separating 2 polygons
    def _inject_intersections(self, points: List[Point]) -> List[Point]:
        result = list(points)
        changed = True

        while changed:
            changed = False
            n = len(result)
            for i in range(n):
                p1, p2 = result[i], result[(i + 1) % n]
                for j in range(i + 2, n):
                    if (i == 0 and j == n - 1):
                        continue
                    p3, p4 = result[j], result[(j + 1) % n]
                    l1 = Line.from_points(p1, p2)
                    l2 = Line.from_points(p3, p4)
                    inter = l1.intersect(l2)
                    if inter:
                        if (inter.is_on_segment(p1, p2) and inter.is_on_segment(p3, p4)):
                            if (inter == p1 or inter == p2 or inter == p3 or inter == p4):
                                continue
                            result.insert(j + 1, inter)
                            result.insert(i + 1, inter)
                            changed = True
                            break
                if changed:
                    break
        return result

    def _process_points(self, points: List[Point]) -> List[Polygon]:
        res = []
        current_points = list(points)

        while len(current_points) >= 3:
            loop_found = False
            for i in range(len(current_points)):
                for j in range(i + 1, len(current_points)):
                    if current_points[i] == current_points[j]:
                        loop = current_points[i:j]
                        poly = Polygon(loop)
                        if poly.area() > 1e-4:
                            res.append(poly)

                        current_points = current_points[:i] + current_points[j:]
                        loop_found = True
                        break
                if loop_found: break
            if not loop_found:
                poly = Polygon(current_points)
                if poly.area() > 1e-4:
                    res.append(poly)
                break

        return res
