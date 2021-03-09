import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from copy import deepcopy

from cell import Cell
from board import Board
from state import State


class Problem():
    def __init__(self, height, width, radius, price_backbone, price_router, budget, backbone, grid):
        self.radius = radius
        self.price_backbone = price_backbone
        self.price_router = price_router
        self.budget = budget

        self.board = Board(height, width, grid)
        self.current_state = State(backbone, self.board)
        self.current_score = self.calc_score(self.current_state)

    def __str__(self):
        return self.board.__str__()

    # Correct?
    def generate_new_states(self):

        for cell in self.current_state.get_backboned_cells():
            new_state = deepcopy(self.current_state)
            new_state.place_router(cell, self.radius)
            yield new_state

        for cell in self.current_state.get_backboned_cells():
            new_state = deepcopy(self.current_state)
            new_state.place_backbone(cell)
            yield new_state

    def normal_hillclimb(self):
        neighbour_states = self.generate_new_states()

        while True:
            neighbour = next(neighbour_states)
            neighbour_score = self.calc_score(neighbour)
            if neighbour_score <= self.current_score:
                return self.current_state

            self.current_state = neighbour
            self.current_score = neighbour_score
            neighbour_states = self.generate_new_states()

    def hillclimb_steepest_ascent(self):

        while True:
            neighbour = max(self.generate_new_states(), key=self.calc_score)
            neighbour_score = self.calc_score(neighbour)
            if neighbour_score <= self.current_score:
                return self.current_state

            self.current_state = neighbour
            self.current_score = neighbour_score

    def calc_score(self, state):
        return 1000 * state.get_covered_targets_amount() + (self.budget - (state.get_placed_backbones_amount() * self.price_backbone) + state.get_placed_routers_amount() * self.price_router)


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
    figure.add_axes(axes)
    axes.imshow(data.grid)
    plt.show()

# Not working


def image(data):
    newimage = Image.fromarray(data.grid)
    # newimage = Image.new(
    #     'RGB', (len(data.grid[0]), len(data.grid)))  # type, size
    # newimage.putdata([tuple(p) for row in data.grid for p in row])
    newimage.save("example.png")  # takes type from filename extension


if __name__ == "__main__":
    p = read_file("input/example.in")

    # result = p.normal_hillclimb()
    result = p.hillclimb_steepest_ascent()
    print(result)
    # plot(p)
