import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

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
        self.state = State(backbone, self.board)

    def __str__(self):
        return self.board.__str__()

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

    print(p)
    print(p.calc_score(p.state))
    # plot(p)
