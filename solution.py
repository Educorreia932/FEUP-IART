import time

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from copy import deepcopy

from cell import Cell
from grid import Grid
from state import State


class Problem:
    def __init__(self, H, W, R, Pb, Pr, budget, backbone, cells):
        self.R = R
        self.Pb = Pb
        self.Pr = Pr
        self.B = budget

        self.grid = Grid(H, W, cells)
        self.current_state = State(backbone, self.grid)
        self.current_score = self.score(self.current_state)

    def __str__(self):
        return self.grid.__str__()

    # Correct?
    def generate_new_states(self):
        for cell in self.current_state.get_backboned_cells():
            new_state = deepcopy(self.current_state)
            new_state.place_router(cell, self.R)
            yield new_state

        for cell in self.current_state.get_backboned_cells():
            new_state = deepcopy(self.current_state)
            new_state.place_backbone(cell)
            yield new_state

    def normal_hillclimb(self):
        neighbour_states = self.generate_new_states()

        while True:
            neighbour = next(neighbour_states)
            neighbour_score = self.score(neighbour)

            if neighbour_score <= self.current_score:
                return self.current_state

            self.current_state = neighbour
            self.current_score = neighbour_score
            neighbour_states = self.generate_new_states()

    def hillclimb_steepest_ascent(self):
        while True:
            neighbour = max(self.generate_new_states(), key=self.score)
            neighbour_score = self.score(neighbour)

            if neighbour_score <= self.current_score:
                return self.current_state

            self.current_state = neighbour
            self.current_score = neighbour_score

    def score(self, state):
        l = state.get_covered_targets_amount()
        N = state.get_placed_backbones_amount()
        M = state.get_placed_routers_amount()

        return 1000 * l + (self.B - N * self.Pb + M * self.Pr)


def read_file(filename):
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

    axes.imshow(data.grid.cells)

    plt.show()


def image(data):
    newimage = Image.fromarray(data.cells)

    newimage.save("example.png")  # takes type from filename extension


if __name__ == "__main__":
    start = time.time()

    p = read_file("input/charleston_road.in")

    result = p.normal_hillclimb()
    # result = p.hillclimb_steepest_ascent()

    plot(result)

    end = time.time()
    print(f"Elapsed time of execution is {end - start} seconds")
