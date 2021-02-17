from grid import TriangleGrid
from typing import Dict, Tuple, List
import matplotlib.pyplot as plt
import numpy as np
import os


def visualize_grid(grid: TriangleGrid, size: int = 1, extra_space: int = 2, folder_name: str = ''):
    __draw_triangles(grid)
    __show_save_visualization(folder_name=folder_name)


def __draw_board(board_shape: Tuple[int, int, int, int], size: int = 1, extra_space: int = 2):
    fig, axs = plt.subplots(1)
    axs.axis('off')
    fig.gca().set_aspect('equal', adjustable='box')

    axs.set_xticks(np.arange(board_shape[0] - extra_space, board_shape[2] + extra_space, 1))
    axs.set_yticks(np.arange(board_shape[1] - extra_space, board_shape[3] + extra_space, 1))

    axs.grid(True, which='both')
    return axs


def __draw_triangles(grid: TriangleGrid):
    axs = __draw_board(grid.get_grid_shape())

    for one, two, three in grid.get_triangles():
        triangle = plt.Polygon([one, two, three])
        axs.add_patch(triangle)


def __show_save_visualization(show_vis: bool = True, save_vis: bool = True, vis_name: str = '', folder_name: str = ''):
    if save_vis:
        if not os.path.exists(f'figures/{folder_name}'):
            os.makedirs(f'figures/{folder_name}')
        plt.title(vis_name)
        plt.savefig(f'figures/{folder_name}/{vis_name}', dpi=300)
    if show_vis:
        if vis_name:
            plt.title(vis_name)
        plt.show()
    plt.close()

