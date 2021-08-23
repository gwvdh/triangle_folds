import matplotlib.pyplot as plt
from typing import List
from grid import Shape, Grid
import numpy as np


def strip_bitstring(bit: int, length) -> str:
    bit = bin(bit).lstrip('0')
    bit = bit.lstrip('b')
    for _ in range(len(bit), length):
        bit = '0' + bit
    return bit


def __draw_pixels(location: Shape, grid: Grid):
    fig, axs = plt.subplots(1)
    axs.axis('off')
    fig.gca().set_aspect('equal', adjustable='box')

    all_folds: List[int] = location.get_all_folds()

    axs.set_xticks(np.arange(-2, grid.strip_length + 2, 1))
    axs.set_yticks(np.arange(-2, len(all_folds) + 2, 1))

    axs.grid(True, which='both')
    # Get all folding sequences and add to plot
    index: int = 0
    # all_folds.sort(key=lambda i: int(strip_bitstring(i, grid.strip_length)[::-1],2))
    all_folds.sort(key=lambda i: strip_bitstring(i, grid.strip_length).count('1'))
    for sequence in all_folds:
        bit_string: str = strip_bitstring(sequence, grid.strip_length)
        for bit_index in range(len(bit_string)):
            if bit_string[bit_index] == '1':
                shape = plt.Polygon([(bit_index, index),
                                     (bit_index, index + 1),
                                     (bit_index + 1, index + 1),
                                     (bit_index + 1, index)], facecolor='black')
                axs.add_patch(shape)
        index += 1
    print('Show plot: {}'.format(location.get_grid_coordinates()))
    plt.show()
    # plt.close()



