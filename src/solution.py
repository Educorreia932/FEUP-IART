import time

import numpy as np
import matplotlib.pyplot as plt

from state import State
from problem import Problem

from os import getcwd

cells = {
    "-": -1,
    "#": 0,
    ".": 1,
}


def read_file(filename) -> Problem:
    with open(filename) as file:
        lines = file.read().split("\n")

        H, W, R = [int(x) for x in lines[0].split()]
        Pb, Pr, B = [int(x) for x in lines[1].split()]
        br, bc = [int(x) for x in lines[2].split()]

        grid = np.zeros((H, W), dtype=np.int8)

        for i in range(H):
            for j in range(W):
                grid[i, j] = cells[lines[i + 3][j]]

        return Problem(H, W, R, Pb, Pr, B, (br, bc), grid)


def plot(data):
    figure = plt.figure()

    axes = plt.Axes(figure, (0, 0, 1, 1))
    axes.axis("off")

    figure.add_axes(axes)

    backbone = data.backbone()
    coverage = data.wireless_coverage()

    axes.imshow(data.grid.cells, vmin=-2, vmax=4)
    axes.imshow(coverage, cmap=plt.cm.gray, alpha=0.2)

    plt.savefig("out/example.png")


if __name__ == "__main__":
    start = time.time()

    # p: Problem = read_file("/input/example.in")
    # p: Problem = read_file("input/charleston_road.in")
    p: Problem = read_file("input/rue_de_londres.in")
    # p: Problem = read_file("input/opera.in")

    print(f"Budget: {p.B}")
    print(f"Price per router: {p.Pr}")
    print(
        f"Number of uncovered targets: {p.current_state.get_uncovered_targets_amount()}")
    print()

    result: State = p.normal_hillclimb()
    # result: State = p.hillclimb_steepest_ascent()
    # result: State = p.simulated_annealing(2)

    end = time.time()

    print(f"This solution is worth {p.score(result)} points.")
    print()
    print(f"Number of covered targets: {result.get_covered_targets_amount()}")
    print(
        f"Number of uncovered targets: {result.get_uncovered_targets_amount()}")
    print(f"Number of placed routers: {result.get_placed_routers_amount()}")
    print()
    print(f"Elapsed time of execution is {end - start} seconds.")

    plot(result)
