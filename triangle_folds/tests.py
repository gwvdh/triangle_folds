import unittest
from grid import TriangleGrid
from visualization import visualize_grid
from enumeration import enumerate_strips_brute_force, enumerate_max_folds
import random
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, List


def draw_board(board_shape: Tuple[int, int, int, int], extra_space: int = 2):
    """
    Draw the figure and set the size of the canvas.

    :param board_shape: Shape and size of the board
    :param extra_space: Extra space to add to the figure
    :return:
    """
    fig, axs = plt.subplots(1)
    axs.axis('off')
    fig.gca().set_aspect('equal', adjustable='box')

    axs.set_xticks(np.arange(board_shape[0] - extra_space, board_shape[2] + extra_space, 1))
    axs.set_yticks(np.arange(board_shape[1] - extra_space, board_shape[3] + extra_space, 1))

    axs.grid(True, which='both')
    return fig, axs


class TestVisualization(unittest.TestCase):
    def test_visualization(self):
        strip_length = 7
        grid: TriangleGrid = TriangleGrid(strip_length)
        for x in range(50):
            for y in range(50):
                grid.add_triangle(x, y, score=random.randint(0, strip_length))
        visualize_grid(grid)


class TestEnumeration(unittest.TestCase):
    def test_brute_force(self):
        enumerate_strips_brute_force([(i, False) for i in range(0, 23)],
                                     is_triangle_grid=True,
                                     count=True,
                                     is_triangle=True,
                                     log_scale=False,
                                     draw_strip=True)

    def test_max_folds(self):
        for i in range(0, 12):
            # print("Computing {}".format(i))
            enumerate_max_folds([(i, False)],
                                is_triangle_grid=True,
                                count=False,
                                is_triangle=True,
                                log_scale=False,
                                draw_strip=True)

    def test_sequence_visualization(self):
        enumerate_strips_brute_force([(i, False) for i in range(12, 16)],
                                     is_triangle_grid=True,
                                     count=True,
                                     is_triangle=True,
                                     log_scale=True,
                                     draw_strip=True)

    def test_board(self):
        fig, axs = draw_board((5, 5, 5, 5))
        shape = plt.Polygon([(1, 0), (3, 3), (4, 1)], facecolor='black')
        axs.add_patch(shape)
        plt.show()
        plt.close()


if __name__ == '__main__':
    unittest.main()
