from grid import TriangleGrid
from typing import Tuple, List
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap, ScalarMappable
from matplotlib.colors import Normalize
import numpy as np
import os


def visualize_grid(grid: TriangleGrid, size: int = 1, extra_space: int = 2,
                   folder_name: str = '', file_name: str = 'visualization'):
    cmap = get_cmap('Spectral', lut=grid.strip_length + 1)
    __draw_triangles(grid, cmap=cmap)
    __show_save_visualization(folder_name=folder_name, vis_name=file_name, show_vis=False)


def __draw_board(board_shape: Tuple[int, int, int, int], size: int = 1, extra_space: int = 2):
    """
    Draw the figure and set the size of the canvas.

    :param board_shape: Shape and size of the board
    :param size:
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


def __draw_triangles(grid: TriangleGrid, cmap=get_cmap('Spectral')):
    """
    Create the figures and draw the triangles with a color map.

    :param grid: The grid containing all triangles with their scores
    :param cmap: The color map. Default is spectral
    :return:
    """
    fig, axs = __draw_board(grid.get_grid_shape())

    fig.colorbar(ScalarMappable(norm=Normalize(vmin=0, vmax=cmap.N), cmap=cmap), ticks=range(cmap.N), ax=axs)

    for t in grid.get_triangles():
        coordinates = t.get_coordinates(grid.side_lengths)
        triangle = plt.Polygon(coordinates, facecolor=cmap(t.get_score()))
        axs.add_patch(triangle)
        # axs.text(*t.get_center(1.), '{}'.format(t.get_score()), fontsize=17)

    __draw_strip(grid, axs)


def __draw_strip(grid: TriangleGrid, axs):
    """
    Draw the strip which we are folding.

    :param grid: The given triangle grid
    :param axs: The figure axes
    :return:
    """
    coordinates: List[Tuple[float, float]] = grid.get_strip_coordinates()
    strip = plt.Polygon(coordinates, edgecolor='black', facecolor='none')
    axs.add_patch(strip)


def __show_save_visualization(show_vis: bool = True, save_vis: bool = True, vis_name: str = '', folder_name: str = ''):
    """
    Show the visualization and save the visualization as a png in folder folder/.

    :param show_vis: Show the visualization in a screen
    :param save_vis: Save the visualization to a file
    :param vis_name: The name of the visualization, which is also the name of the file
    :param folder_name: The name of the folder to put the figure in
    :return:
    """
    if save_vis:
        if not os.path.exists(f'figures/{folder_name}'):
            os.makedirs(f'figures/{folder_name}')
        # plt.title(vis_name)
        plt.savefig(f'figures/{folder_name}/{vis_name}', dpi=300)
    if show_vis:
        if vis_name:
            plt.title(vis_name)
        plt.show()
    plt.close()
