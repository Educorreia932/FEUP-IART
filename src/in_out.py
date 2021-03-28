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

    figure.add_axes(axes)

    cells = backbone(solution)

    axes.imshow(cells, vmin=-2, vmax=4)
    axes.imshow(solution.coverage.clip(0,1), cmap=plt.cm.gray, alpha=0.2)

    print(f"Covered cells {solution.covered_cells}")
    print(f"Placed routers {len(solution.get_placed_routers())}")

    plt.savefig("out/grid.png")
    plt.show()

def backbone(solution: Solution):
    g = solution.graph
    grid = solution.problem.grid

    for router in g.result:
        start = g.vertices[router[0]]
        target = g.vertices[router[1]]

        grid.place_router(start)

        if start[0] == target[0]:
            s = min((start[1], target[1]))
            e = max((start[1], target[1]))

            for j in range(s, e):
                if j != start[1]:
                    grid.place_cable((start[0], j))

        elif start[1] == target[1]:
            s = min((start[0], target[0]))
            e = max((start[0], target[0]))

            for i in range(s, e):
                if i != start[0]:
                    grid.place_cable((i, start[1]))

        else:
            if (target[0] - start[0]) < 0:
                xdiff = -1

            elif (target[0] - start[0]) > 0:
                xdiff = 1

            else:
                xdiff = 0

            if (target[1] - start[1]) < 0:
                ydiff = -1

            elif (target[1] - start[1]) > 0:
                ydiff = 1

            else:
                ydiff = 0

            delta = (xdiff, ydiff)
            current_cell = (start[0], start[1])

            while current_cell[0] != target[0] and current_cell[1] != target[1]:
                current_cell = (
                    current_cell[0] + delta[0], current_cell[1] + delta[1])

                if current_cell == target:
                    break

                else:
                    grid.place_cable(current_cell)

            if current_cell != target:
                if current_cell[0] == target[0]:
                    s = min((current_cell[1], target[1]))
                    e = max((current_cell[1], target[1]))

                    for j in range(s, e):
                        if j != s:
                            grid.place_cable((current_cell[0], j))

                if current_cell[1] == target[1]:
                    s = min((current_cell[0], target[0]))
                    e = max((current_cell[0], target[0]))

                    for i in range(s, e):
                        if i != s:
                            grid.place_cable((i, current_cell[1]))

    return grid.cells
