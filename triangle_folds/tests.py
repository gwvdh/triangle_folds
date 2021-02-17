import unittest
from grid import TriangleGrid, Triangle
from visualization import visualize_grid


class TestVisualization(unittest.TestCase):
    def test_visualization(self):
        grid: TriangleGrid = TriangleGrid(3)
        for x in range(50):
            for y in range(50):
                grid.add_triangle(x, y)
        visualize_grid(grid)


if __name__ == '__main__':
    unittest.main()
