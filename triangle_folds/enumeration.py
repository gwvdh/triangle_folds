from typing import List, Tuple
from grid import TriangleGrid, Triangle
from visualization import visualize_grid


def enumerate_strips(strips: List[Tuple[int, bool]]):
    """
    Visualize all given problem instances.
    This is done using brute force.
    We enumerate every possible combination of folds, represented as a bit string.

    :param strips: List of problem instances represented by strip length and orientation
    :return: Creates figures in figures/
    """
    for length, flipped in strips:
        grid = TriangleGrid(length, flipped)
        start: Tuple[int, int] = (0, 1 if flipped else 0)
        for i in range(2 ** length):
            fold_amount: int = bin(i).count('1')
            if fold_amount <= 4:
                add_coordinate_to_grid(grid, i, start, length)
        max_folds: int = 0
        for _, triangle in grid.grid.items():
            if triangle.get_score() > max_folds:
                max_folds = triangle.get_score()
        visualize_grid(grid, file_name='triangle_length_{}_flipped_{}_max_{}'.format(length, flipped, max_folds))


def is_upside_down(x: int, y: int):
    return (y % 2 == 1) != (x % 2 == 1)


def add_coordinate_to_grid(grid: TriangleGrid, bit: int, start: Tuple[int, int], length: int) -> int:
    fold_amount: int = bin(bit).count('1')
    coordinate: Tuple[int, int] = get_coordinate(bit, start, length)
    if coordinate in grid.grid:
        triangle: Triangle = grid.get_triangle(*coordinate)
        if triangle.get_score() > fold_amount:
            triangle.set_score(fold_amount)
            triangle.set_fold(bit)
    else:
        grid.add_triangle(*coordinate, fold_amount)
        grid.get_triangle(*coordinate).set_fold(bit)
    return fold_amount


def enumerate_max_folds(strips: List[Tuple[int, bool]], max_folds: int = 4):
    """
    Visualize all given problem instances.
    We enumerate every possible combination of folds with a maximum amount of folds,
    represented as a bit string.

    :param strips: List of problem instances represented by strip length and orientation
    :param max_folds: Maximum amount of folds
    :return: Creates figures in figures/
    """
    for length, flipped in strips:
        grid = TriangleGrid(length, flipped)
        start: Tuple[int, int] = (0, 1 if flipped else 0)
        current_int: int = 0
        while current_int < 2 ** length:
            fold_amount: int = add_coordinate_to_grid(grid, current_int, start, length)
            if fold_amount < max_folds:
                current_int += 1
            else:
                shift_number: int = len(bin(current_int)) - len(bin(current_int).rstrip('0'))
                current_int = current_int >> shift_number
                current_int += 1
                current_int = current_int << shift_number
        max_folds: int = 0
        for _, triangle in grid.grid.items():
            if triangle.get_score() > max_folds:
                max_folds = triangle.get_score()
        visualize_grid(grid, file_name='triangle_length_{}_flipped_{}_max_{}'.format(length, flipped, max_folds))


def get_coordinate(bit_string: int, start: Tuple[int, int], length: int) -> Tuple[int, int]:
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
