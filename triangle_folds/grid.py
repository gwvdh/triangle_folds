from typing import Dict, Tuple, List
from math import sqrt
from enum import Enum


Fold = Enum('Folds', 'M V')


def get_height(side_length: float) -> float:
    return side_length * sqrt(3) / 2


class Triangle:
    def __init__(self, x: int, y: int, strip_length: int):
        self._x: int = x
        self._y: int = y
        self._score: int = -1
        self._folds: List[str] = ["." for _ in range(strip_length)]

    def set_score(self, score: int):
        self._score = score

    def get_score(self) -> int:
        return self._score

    def get_folds(self) -> List[str]:
        return self._folds

    def set_fold(self, count: int, fold: Fold):
        self._folds[count] = fold.name

    def is_upside_down(self):
        return (self._y % 2 == 1) != (self._x % 2 == 1)

    def get_coordinates(self, length: float) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
        """
           2
          / \
         /   \
        1-----3
        :return:
        """
        height: float = get_height(side_length=length)
        upside_down: bool = self.is_upside_down()
        one = (length * float(self._x) / 2, float(self._y) * height + (height if upside_down else 0))
        two = (length * float(self._x) / 2 + length / 2, float(self._y) * height + (0 if upside_down else height))
        three = (length * float(self._x) / 2 + length, float(self._y) * height + (height if upside_down else 0))
        return one, two, three


class TriangleGrid:
    def __init__(self, strip_length: int, upside_down: bool = False):
        self.strip_length: int = strip_length
        self._upside_down: bool = upside_down
        self.grid: Dict[Tuple[int, int], Triangle] = {}

    def get_triangle(self, x: int, y: int) -> Triangle:
        return self.grid.get((x, y))

    def add_triangle(self, x: int, y: int, score: int = -1):
        triangle: Triangle = Triangle(x, y, self.strip_length)
        triangle.set_score(score)
        self.grid[(x, y)] = triangle

    def get_grid_shape(self) -> Tuple[int, int, int, int]:
        min_x: int = 1
        min_y: int = 1
        max_x: int = 0
        max_y: int = 0
        for (x, y), _ in self.grid.items():
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return min_x, min_y, max_x, max_y

    def get_triangles(self) -> List[Triangle]:
        return [triangle for _, triangle in self.grid.items()]

    def get_triangle_coordinates(self) -> List[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]]:
        triangles: List[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]] = []
        for _, triangle in self.grid.items():
            triangles.append(triangle.get_coordinates(1))
        return triangles

    def get_strip_coordinates(self) -> List[Tuple[float, float]]:
        row: int = 1 if self._upside_down else 0
        start_triangle: Triangle = Triangle(0, row, strip_length=self.strip_length)
        start_coordinates = start_triangle.get_coordinates(1)
        end_triangle: Triangle = Triangle(self.strip_length, row, strip_length=self.strip_length)
        end_coordinates = end_triangle.get_coordinates(1)
        coordinates: List[Tuple[float, float]] = [start_coordinates[0], start_coordinates[1]]
        if start_triangle.is_upside_down():
            if end_triangle.is_upside_down():
                coordinates.append(end_coordinates[1])
                coordinates.append(end_coordinates[2])
            else:
                coordinates.append(end_coordinates[2])
                coordinates.append(end_coordinates[1])
        else:
            if end_triangle.is_upside_down():
                coordinates.append(end_coordinates[2])
                coordinates.append(end_coordinates[1])
            else:
                coordinates.append(end_coordinates[1])
                coordinates.append(end_coordinates[2])

        return coordinates


