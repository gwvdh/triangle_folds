from typing import List, Tuple
from grid import TriangleGrid, Grid, SquareGrid, Shape
from visualization import visualize_grid


def enumerate_strips_brute_force(strips: List[Tuple[int, bool]], is_triangle_grid=True, count: bool = False,
                                 is_triangle: bool = True, log_scale: bool = False, draw_strip: bool = True):
    """
    Visualize all given problem instances.
    This is done using brute force.
    We enumerate every possible combination of folds, represented as a bit string.

    :param strips: List of problem instances represented by strip length and orientation
    :param is_triangle_grid:
    :param count:
    :param is_triangle:
    :param log_scale:
    :param draw_strip:
    :return: Creates figures in figures/
    """
    for length, flipped in strips:
        if is_triangle_grid:
            grid: Grid = TriangleGrid(length, side_lengths=1.0, upside_down=flipped)
        else:
            grid: Grid = SquareGrid(length, side_lengths=1.0)
        start: Tuple[int, int] = (0, 1 if flipped else 0)
        for i in range(2 ** length):
            add_coordinate_to_grid(grid, i, start, length, count=count, is_triangle=is_triangle)
        visualization(grid, length, is_triangle_grid, count, is_triangle, log_scale, draw_strip)


def visualization(grid: Grid, length: int, is_triangle_grid=True, count: bool = False,
                  is_triangle: bool = True, log_scale: bool = False, draw_strip: bool = True):
    max_folds: int = 0
    for _, triangle in grid.grid.items():
        if triangle.get_score() > max_folds:
            max_folds = triangle.get_score()
    file_name = '{}_max_{}_{}_{}_{}{}'.format(length,
                                              max_folds,
                                              'count' if count else 'min',
                                              'triangle' if is_triangle else 'square',
                                              'triangle-grid' if is_triangle_grid else 'square-grid',
                                              '_log' if log_scale else ''
                                              )
    visualize_grid(grid, file_name=file_name, log_scale=log_scale, draw_strip=draw_strip)


def is_upside_down(x: int, y: int):
    return (y % 2 == 1) != (x % 2 == 1)


def add_coordinate_to_grid(grid: Grid, bit: int, start: Tuple[int, int], length: int,
                           count: bool = False, is_triangle: bool = True) -> int:
    fold_amount: int = bin(bit).count('1')
    if is_triangle:
        coordinate: Tuple[int, int] = get_triangle_coordinate(bit, start, length)
    else:
        coordinate: Tuple[int, int] = get_square_coordinate(bit, start, length)
    if coordinate in grid.grid:
        shape: Shape = grid.get_shape(*coordinate)
        if count:
            shape.set_score(shape.get_score() + 1)
        else:
            if shape.get_score() > fold_amount:
                shape.set_score(fold_amount)
        if shape.get_score() > fold_amount:
            shape.set_folds(bit)
    else:
        grid.add_shape(*coordinate, fold_amount)
        grid.get_shape(*coordinate).set_folds(bit)
    return fold_amount


def enumerate_max_folds(strips: List[Tuple[int, bool]], max_folds: int = 4, is_triangle_grid=True, count: bool = False,
                        is_triangle: bool = True, log_scale: bool = False, draw_strip: bool = True):
    """
    Visualize all given problem instances.
    We enumerate every possible combination of folds with a maximum amount of folds,
    represented as a bit string.

    :param strips: List of problem instances represented by strip length and orientation
    :param max_folds: Maximum amount of folds
    :param is_triangle_grid:
    :param count:
    :param is_triangle:
    :param log_scale:
    :param draw_strip:
    :return: Creates figures in figures/
    """
    for length, flipped in strips:
        if is_triangle_grid:
            grid = TriangleGrid(length)
        else:
            grid = SquareGrid(length)
        start: Tuple[int, int] = (0, 1 if flipped else 0)
        current_int: int = 0
        while current_int < 2 ** length:
            fold_amount: int = add_coordinate_to_grid(grid, current_int, start, length,
                                                      count=count, is_triangle=is_triangle)
            if fold_amount < max_folds:
                current_int += 1
            else:
                shift_number: int = len(bin(current_int)) - len(bin(current_int).rstrip('0'))
                current_int = current_int >> shift_number
                current_int += 1
                current_int = current_int << shift_number
        visualization(grid, length, is_triangle_grid, count, is_triangle, log_scale, draw_strip)


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
            if crease % 2 == 0:
                direction = 'B' if direction == 'D' else 'D'
            else:
                direction = 'B' if direction == 'U' else 'U'
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
