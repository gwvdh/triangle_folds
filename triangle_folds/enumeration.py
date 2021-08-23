from typing import List, Tuple
from grid import TriangleGrid, Grid, SquareGrid
from visualization import visualize_grid
# from data_visualization import __draw_pixels


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
            grid.add_coordinate(i, start, length, count=count, is_triangle=is_triangle)
        visualization(grid, length, is_triangle_grid, count, is_triangle, log_scale, draw_strip)
        # print(len(grid.get_shape(0, 0).get_all_folds()))


def reverse_bit(original_bit: int, length: int) -> int:
    bit = bin(original_bit).lstrip('0')
    bit = bit.lstrip('b')
    bit = bit[::-1]
    for _ in range(len(bit), length):
        bit = bit + '0'
    return int(bit, 2)


def strip_bitstring(bit: int, length) -> str:
    bit = bin(bit).lstrip('0')
    bit = bit.lstrip('b')
    for _ in range(len(bit), length):
        bit = '0' + bit
    return bit


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
            fold_amount: int = grid.add_coordinate(current_int, start, length,
                                                   count=count, is_triangle=is_triangle)
            if fold_amount < max_folds:
                current_int += 1
            else:
                shift_number: int = len(bin(current_int)) - len(bin(current_int).rstrip('0'))
                current_int = current_int >> shift_number
                current_int += 1
                current_int = current_int << shift_number
        visualization(grid, length, is_triangle_grid, count, is_triangle, log_scale, draw_strip)
