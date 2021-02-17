from typing import Dict, Tuple, List
from math import sqrt


def get_height(side_length: float) -> float:
    """
    Get the height of an equilateral triangle given the side lengths.

    :param side_length: The lengths of any side
    :return: The height of the triangle
    """
    return side_length * sqrt(3) / 2


class Triangle:
    def __init__(self, x: int, y: int):
        self._x: int = x
        self._y: int = y
        self._score: int = 100
        self._fold_sequence: int = -1

    def set_score(self, score: int):
        self._score = score

    def get_score(self) -> int:
        return self._score

    def get_folds(self) -> int:
        return self._fold_sequence

    def set_fold(self, fold: int):
        self._fold_sequence = fold

    def is_upside_down(self) -> bool:
        """
        Check whether the current triangle is upside down.

        :return: A boolean indicating if the triangle is upside down
        """
        return (self._y % 2 == 1) != (self._x % 2 == 1)

    def get_coordinates(self, length: float) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
        """
        Retrieve the coordinates for each of the corners of the triangle given the lengths of the sides.
        The grid coordinates are given in the object.
        The order of the corners is given in the figure below.
           2      1-----3
          / \  or  \   /
         /   \      \ /
        1-----3      2

        :param length: The lengths of any side
        :return: A tuple of coordinates for each of the corners of the triangle
        """
        height: float = get_height(side_length=length)
        upside_down: bool = self.is_upside_down()
        one = (length * float(self._x) / 2, float(self._y) * height + (height if upside_down else 0))
        two = (length * float(self._x) / 2 + length / 2, float(self._y) * height + (0 if upside_down else height))
        three = (length * float(self._x) / 2 + length, float(self._y) * height + (height if upside_down else 0))
        return one, two, three

    def get_center(self, length: float) -> Tuple[float, float]:
        """
        Get the center of the triangle.

        :param length: The length of any side
        :return: The coordinate of the center
        """
        height: float = get_height(side_length=length)
        base = (length * float(self._x) / 2, float(self._y) * height)
        return base[0] + length / 2, base[1] + height / 2


class TriangleGrid:
    def __init__(self, strip_length: int, upside_down: bool = False, side_lengths: float = 1.0):
        self.strip_length: int = strip_length
        self._upside_down: bool = upside_down
        self.side_lengths: float = side_lengths
        self.grid: Dict[Tuple[int, int], Triangle] = {}

    def get_triangle(self, x: int, y: int) -> Triangle:
        return self.grid.get((x, y))

    def add_triangle(self, x: int, y: int, score: int = 100):
        """
        Add a triangle to the data structure.
        A score is also added.

        :param x: x-coordinate
        :param y: y-coordinate
        :param score: Score representing the amount of folds
        :return:
        """
        triangle: Triangle = Triangle(x, y)
        triangle.set_score(score)
        self.grid[(x, y)] = triangle

    def get_grid_shape(self) -> Tuple[int, int, int, int]:
        """
        Get the min and max coordinates of the triangle grid.

        :return: A tuple consisting of the minimum and maximum x- and y-coordinates
        """
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
            triangles.append(triangle.get_coordinates(self.side_lengths))
        return triangles

    def get_strip_coordinates(self) -> List[Tuple[float, float]]:
        """
        Get the coordinates of a strip of the given length.
        The coordinates indicate the corners of the parallelogram.

        :return: A list of tuples representing the corners of the strip
        """
        row: int = 1 if self._upside_down else 0
        start_triangle: Triangle = Triangle(0, row)
        start_coordinates = start_triangle.get_coordinates(self.side_lengths)
        end_triangle: Triangle = Triangle(self.strip_length, row)
        end_coordinates = end_triangle.get_coordinates(self.side_lengths)
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
