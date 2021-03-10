import time

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from cell import Cell
from state import State
from problem import Problem


# TODO: Move to IO file
def read_file(filename) -> Problem:
    with open(filename) as file:
        lines = file.read().split("\n")

        H, W, R = [int(x) for x in lines[0].split()]
        Pb, Pr, B = [int(x) for x in lines[1].split()]
        br, bc = [int(x) for x in lines[2].split()]

        grid = np.zeros((H, W), dtype=np.int8)

        for i in range(H):
            for j in range(W):
                grid[i, j] = Cell.from_character(lines[i + 3][j])

        return Problem(H, W, R, Pb, Pr, B, (br, bc), grid)


def plot(data):
    figure = plt.figure()

    axes = plt.Axes(figure, (0, 0, 1, 1))
    axes.axis("off")

    figure.add_axes(axes)

    coverage = data.wireless_coverage()

    axes.imshow(data.grid.cells, vmin=-2, vmax=4)
    axes.imshow(coverage, cmap=plt.cm.gray, alpha=0.2)

    plt.show()


def image(data):
    newimage = Image.fromarray(data.cells)

    newimage.save("example.png")  # Takes type from filename extension


if __name__ == "__main__":
    start = time.time()

    p: Problem = read_file("../input/charleston_road.in")

    result: State = p.normal_hillclimb()
    # result: State = p.hillclimb_steepest_ascent()

    end = time.time()

    print(f"This solution is worth {p.score(result)} points.")
    print(f"Elapsed time of execution is {end - start} seconds.")

    plot(result)
