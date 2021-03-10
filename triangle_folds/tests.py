import unittest
from grid import TriangleGrid
from visualization import visualize_grid
from enumeration import enumerate_strips_brute_force, enumerate_max_folds
import random


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
        for i in range(0, 24):
            print("Computing {}".format(i))
            enumerate_strips_brute_force([(i, False)],
                                         is_triangle_grid=True,
                                         count=True,
                                         is_triangle=True,
                                         log_scale=False,
                                         draw_strip=True)

    def test_max_folds(self):
        for i in range(10, 15):
            print("Computing {}".format(i))
            enumerate_max_folds([(i, False)], 5,
                                is_triangle_grid=False,
                                count=False,
                                is_triangle=False,
                                log_scale=False,
                                draw_strip=True)


if __name__ == '__main__':
    unittest.main()
