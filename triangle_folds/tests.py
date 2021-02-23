import unittest
from grid import TriangleGrid, Triangle
from visualization import visualize_grid
from enumeration import enumerate_strips, enumerate_max_folds
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
        for i in range(21,30):
            print("Computing {}".format(i))
            enumerate_strips([(i, False)])

    def test_max_folds(self):
        for i in range(19, 20):
            print("Computing {}".format(i))
            enumerate_max_folds([(i, False)], 5)


if __name__ == '__main__':
    unittest.main()
