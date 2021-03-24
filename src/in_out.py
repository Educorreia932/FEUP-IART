import matplotlib.pyplot as plt
import numpy as np

from problem import *
from grid import *

def read_file(filename) -> Problem:
    with open(filename) as file:
        lines = file.read().split("\n")

        H, W, R = [int(x) for x in lines[0].split()]
        Pb, Pr, B = [int(x) for x in lines[1].split()]
        br, bc = [int(x) for x in lines[2].split()]

        cells = np.zeros((H, W), dtype=np.int8)

        for i in range(H):
            for j in range(W):
                cells[i, j] = CELL_TYPE[lines[i + 3][j]]

        return Problem(H, W, R, Pb, Pr, B, (br, bc), Grid(cells))

def plot(solution: Solution) -> None:
    figure = plt.figure()

    axes = plt.Axes(figure, (0, 0, 1, 1))
    axes.axis("off")

    plt.savefig("out/example.png")
    plt.show()
