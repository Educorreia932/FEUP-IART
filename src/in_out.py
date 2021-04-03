import matplotlib.pyplot as plt
import numpy as np

from functools import partial
from problem import *
from grid import *

def user_input() -> tuple:
    """
    Get user input selection for the building to be considered to the problem and the algorithm to be used.
    """

    buildings = [
        "input/example.in",
        "input/charleston_road.in",
        "input/rue_de_londres.in",
        "input/opera.in",
        "input/lets_go_higher.in"
    ]

    algorithms = [
        Problem.hill_climbing,
        Problem.hill_climbing_steepest_ascent,
        Problem.simulated_annealing,
        partial(Problem.genetic_algorithm, crossover=1),
        partial(Problem.genetic_algorithm, crossover=2)
    ]

    print("Select the building:")
    print("[1] Example")
    print("[2] Charleston Road")
    print("[3] Rue de Londres")
    print("[4] Opera")
    print("[5] Let's Go Higher")

    selected_building = int(input()) - 1

    print()
    print("Select the optimization algorithm:")
    print("[1] Hill Climbing")
    print("[2] Hill Climbing - Steepest Ascent")
    print("[3] Simmulated Annealing")
    print("[4] Genetic Algorithm - Crossover 1")
    print("[5] Genetic Algorithm - Crossover 2")
    print()

    selected_algorithm = int(input()) - 1

    return buildings[selected_building], algorithms[selected_algorithm]

def read_file(filename: str) -> Problem:
    """
    Read problem information from input file.
    """
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
    """
    Plot the resulting solution building grid.
    """

    figure = plt.figure()

    axes = plt.Axes(figure, (0, 0, 1, 1))
    axes.axis("off")

    figure.add_axes(axes)

    cells = backbone(solution)

    axes.imshow(cells, vmin=-2, vmax=4)
    # solution.calculate_initial_coverage()
    axes.imshow(solution.coverage.clip(0, 1), cmap=plt.cm.gray, alpha=0.2)

    plt.savefig("out/grid.png")
    plt.show()

def backbone(solution: Solution) -> np.array:
    """
    Place cable and router cells in grid after solving the problem.
    This is necessary to plot the resulting building grid.
    """

    g = solution.graph
    grid = solution.problem.grid
    grid.place_backbone(solution.problem.b)

    # Place the router cells in the building grid
    for router in solution.get_placed_routers():
        grid.place_router(router)

    # For each router in the resulting MST plot its wireless range
    for router in g.result:
        start = g.vertices[router[0]]
        target = g.vertices[router[1]]

        if start[0] == target[0]:
            s = min((start[1], target[1]))
            e = max((start[1], target[1]))

            for j in range(s, e):
                if j != s:
                    grid.place_cable((start[0], j))

        elif start[1] == target[1]:
            s = min((start[0], target[0]))
            e = max((start[0], target[0]))

            for i in range(s, e):
                if i != s:
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
