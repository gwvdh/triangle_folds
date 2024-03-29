from typing import Dict, Tuple, List
from math import sqrt, floor, ceil
from abc import abstractmethod


def is_upside_down(x: int, y: int):
    return (y % 2 == 1) != (x % 2 == 1)


def get_height(side_length: float) -> float:
    """
    Get the height of an equilateral triangle given the side lengths.

    :param side_length: The lengths of any side
    :return: The height of the triangle
    """
    return side_length * sqrt(3) / 2


def get_triangle_coordinate(bit_string: int, start: Tuple[int, int], length: int) -> Tuple[int, int]:
    """
    Find the coordinate given a bit string (as an integer) representing folds.

    :param bit_string: The bit string representing folds
    :param start: Starting coordinate of the (static) first triangle
    :param length: The length of the strip
    :return: The coordinate of the final triangle in the strip when all folds are folded
    """
    direction: str = 'B'  # 'B'; base, 'U'; up, 'D'; down
    x_coordinate: int = start[0]
    y_coordinate: int = start[1]
    for crease in range(length):
        if bit_string & (1 << crease):  # If the ith crease is folded
            if is_upside_down(x_coordinate, y_coordinate):
                if direction == 'B':
                    direction = 'U'
                elif direction == 'U':
                    direction = 'D'
                else:
                    direction = 'B'
            else:
                if direction == 'B':
                    direction = 'D'
                elif direction == 'U':
                    direction = 'B'
                else:
                    direction = 'U'
        else:
            if direction == 'B':
                x_coordinate += 1
            elif direction == 'U':
                if is_upside_down(x_coordinate, y_coordinate):
                    y_coordinate += 1
                else:
                    x_coordinate -= 1
            elif direction == 'D':
                if is_upside_down(x_coordinate, y_coordinate):
                    x_coordinate -= 1
                else:
                    y_coordinate -= 1
            else:
                raise ValueError('Direction {} does not exist'.format(direction))
    return x_coordinate, y_coordinate


def get_square_coordinate(bit_string: int, start: Tuple[int, int], length: int) -> Tuple[int, int]:
    direction: str = 'NE'
    x_coordinate: int = start[0]
    y_coordinate: int = start[1]
    for crease in range(length):
        if bit_string & (1 << crease):
            if crease % 2 == 0:
                if 'N' in direction:
                    direction = direction.replace('N', 'S')
                else:
                    direction = direction.replace('S', 'N')
            else:
                if 'W' in direction:
                    direction = direction.replace('W', 'E')
                else:
                    direction = direction.replace('E', 'W')
        else:
            if crease % 2 == 0:
                if 'N' in direction:
                    y_coordinate = y_coordinate + 1
                else:
                    y_coordinate = y_coordinate - 1
            else:
                if 'E' in direction:
                    x_coordinate = x_coordinate + 1
                else:
                    x_coordinate = x_coordinate - 1
    return x_coordinate, y_coordinate


class Shape:
    def __init__(self, x: int, y: int):
        self._x: int = x
        self._y: int = y
        self._score: int = 100
        self._fold_sequence: int = int('1'*90, 2)
        self._all_folds: List[int] = []

    def get_grid_coordinates(self):
        return self._x, self._y

    def set_score(self, score: int):
        self._score = score

    def get_score(self) -> int:
        return self._score

    def get_folds(self) -> int:
        return self._fold_sequence

    def get_all_folds(self) -> List[int]:
        return self._all_folds

    def set_folds(self, fold: int):
        if bin(fold).count('1') < bin(self._fold_sequence).count('1'):
            self._fold_sequence = fold
        self._all_folds.append(fold)

    @abstractmethod
    def get_coordinates(self, length: float):
        raise NotImplemented

    @abstractmethod
    def get_center(self, length: float):
        raise NotImplemented


class Triangle(Shape):
    def is_upside_down(self) -> bool:
        """
        Check whether the current triangle is upside down.

        :return: A boolean indicating if the triangle is upside down
        """
        return (self._y % 2 == 1) != (self._x % 2 == 1)

    def get_coordinates(self, length: float) -> List[Tuple[float, float]]:
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
        return [one, two, three]

    def get_center(self, length: float) -> Tuple[float, float]:
        """
        Get the center of the triangle.

        :param length: The length of any side
        :return: The coordinate of the center
        """
        height: float = get_height(side_length=length)
        base = (length * float(self._x) / 2, float(self._y) * height)
        return base[0] + length / 2, base[1] + height / 2


class Grid:
    def __init__(self, strip_length: int, side_lengths: float = 1.0):
        self.strip_length: int = strip_length
        self.side_lengths: float = side_lengths
        self.grid: Dict[Tuple[int, int], Shape] = {}

    def adjacency_matrix(self) -> Dict[Tuple[Shape, Shape], int]:
        matrix: Dict[Tuple[Shape, Shape], int] = {}
        for _, shape_1 in self.grid.items():
            for _, shape_2 in self.grid.items():
                fold_amount: int = bin(shape_1.get_folds() ^ shape_2.get_folds()).count('1')
                matrix[(shape_1, shape_2)] = fold_amount
        return matrix

    def print_adjacency_matrix(self):
        matrix: Dict[Tuple[Shape, Shape], int] = self.adjacency_matrix()
        for shapes, dist in matrix.items():
            if dist > 6:
                raise ValueError

    def get_max_score(self) -> int:
        max_score: int = 0
        for _, shape in self.grid.items():
            if shape.get_score() > max_score:
                max_score = shape.get_score()
        return max_score

    def get_max_score_shape(self) -> Shape:
        max_score: int = 0
        max_shape: Shape or None = None
        for _, shape in self.grid.items():
            if shape.get_score() > max_score:
                max_score = shape.get_score()
                max_shape = shape
        if max_shape is None:
            raise ValueError
        return max_shape

    def get_shape(self, x: int, y: int) -> Shape:
        return self.grid.get((x, y))

    def get_shapes(self) -> List[Shape]:
        return [shape for _, shape in self.grid.items()]

    @abstractmethod
    def get_strip_coordinates(self) -> List[Tuple[float, float]]:
        pass

    @abstractmethod
    def add_shape(self, x: int, y: int, score: int = 100):
        """
        Add a shape to the data structure.
        A score is also added.

        :param x: x-coordinate
        :param y: y-coordinate
        :param score: Score representing the amount of folds
        :return:
        """
        pass

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

    def add_coordinate(self, bit: int, start: Tuple[int, int], length: int,
                       count: bool = False, is_triangle: bool = True) -> int:
        fold_amount: int = bin(bit).count('1')
        if is_triangle:
            coordinate: Tuple[int, int] = get_triangle_coordinate(bit, start, length)
        else:
            coordinate: Tuple[int, int] = get_square_coordinate(bit, start, length)
        if coordinate in self.grid:
            shape: Shape = self.get_shape(*coordinate)
            if count:
                shape.set_score(shape.get_score() + 1)
            else:
                if shape.get_score() > fold_amount:
                    shape.set_score(fold_amount)
            shape.set_folds(bit)
        else:
            self.add_shape(*coordinate, fold_amount)
            self.get_shape(*coordinate).set_folds(bit)
        return fold_amount


class TriangleGrid(Grid):
    def __init__(self, strip_length: int, side_lengths: float = 1.0, upside_down: bool = False):
        super().__init__(strip_length, side_lengths)
        self._upside_down: bool = upside_down

    def add_shape(self, x: int, y: int, score: int = 100):
        triangle: Triangle = Triangle(x, y)
        triangle.set_score(score)
        self.grid[(x, y)] = triangle

    def add_triangle(self, x: int, y: int, score: int = 100):
        self.add_shape(x, y, score)

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

    def get_strip_triangles(self):
        return [self.grid[(i, 0)] for i in range(self.strip_length, 0, -1)]


class Square(Shape):
    def get_coordinates(self, length: float) -> List[Tuple[float, float]]:
        """
        Return a list of rectangle coordinates.
        :param length: Length of all sides of the square
        :return: A list of coordinates representing the corners of the square
        """
        return [(self._x + dx * length, self._y + dy * length) for dx, dy in [(0, 0), (1, 0), (1, 1), (0, 1)]]

    def get_center(self, length: float) -> Tuple[float, float]:
        """
        Get the center of the square.
        :param length: Length of all sides of the square
        :return: A tuple representing the coordinates of the center of the square
        """
        return self._x + length / 2, self._y + length / 2


class SquareGrid(Grid):
    def add_shape(self, x: int, y: int, score: int = 100):
        square: Square = Square(x, y)
        square.set_score(score)
        self.grid[(x, y)] = square

    def add_square(self, x: int, y: int, score: int = 100):
        self.add_shape(x, y, score)

    def get_strip_coordinates(self) -> List[Tuple[float, float]]:
        """
        Get the coordinates of a strip of the given length.
        The coordinates indicate the corners of the polygon.

        :return: A list of tuples representing the corners of the polygon
        """
        bottom: List[Tuple[float, float]] = [
            ((floor(i / 2) + 1) * self.side_lengths, ceil(i / 2) * self.side_lengths)
            for i in range(self.strip_length + 1)
        ]
        top: List[Tuple[float, float]] = [
            (floor(i / 2) * self.side_lengths, (ceil(i / 2) + 1) * self.side_lengths)
            for i in range(self.strip_length + 1)
        ]
        top.insert(0, (0, 0))
        top.append((floor(self.strip_length / 2 + 1) * self.side_lengths,
                    ceil(self.strip_length / 2 + 1) * self.side_lengths))
        bottom.reverse()
        top.extend(bottom)
        return top
