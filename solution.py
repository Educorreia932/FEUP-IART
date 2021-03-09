import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from cell import Cell
from board import Board

class Problem():
    def __init__(self, height, width, radius, price_backbone, price_router, budget, backbone, grid):
        self.board = Board(height, width, grid)

        self.radius = radius
        self.price_backbone = price_backbone
        self.price_router = price_router
        self.budget = budget

    def __str__(self):
        result = ""
        for line in self.grid:
            for elem in line:
                result += Cell.to_character(elem) + " "
            result += "\n"

        return result

    # ineficiente
    def router_can_see(self, r_coords, target):
        top = min(target[0], r_coords[0])
        bottom = max(target[0], r_coords[0])

        left = min(target[1], r_coords[1])
        right = max(target[1], r_coords[1])

        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                if self.grid[i][j] == Cell.WALL:
                    return False

        return True

    def place_router(self, coords):
        self.grid[coords[0]][coords[1]] = Cell.ROUTER

        for i in range(coords[0] - self.radius, coords[0] + self.radius + 1):
            for j in range(coords[1] - self.radius, coords[1] + self.radius + 1):
                if self.router_can_see(coords, [i, j]) and coords != [i, j]:
                    if self.grid[i][j] == Cell.TARGET:
                        self.target_covered += 1 
                    self.grid[i][j] = Cell.CONNECTED_ROUTER

    def place_backbone(self, coords):
        self.grid[coords[0]][coords[1]] = Cell.BACKBONE
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= i < self.height and 0 <= j < self.width and i != j and self.grid[coords[0]][coords[1]] != Cell.WALL:
                    self.connected_cells.append([coords[0] + i, coords[1] + j])

    def score(self):
        return 1000 * self.target_covered + (self.budget - (len(self.placed_backbones) * self.price_backbone) + len(self.placed_routers) * self.price_router)


def read_file(filename):
    with open(filename) as file:
        lines = file.read().split("\n")

        H, W, R = [int(x) for x in lines[0].split()]
        Pb, Pr, B = [int(x) for x in lines[1].split()]
        br, bc = [int(x) for x in lines[2].split()]

        grid = []

        for i in range(3, H + 3):
            aux = []
            for j in range(W):
                aux.append(Cell.from_character(lines[i][j]))
            grid.append(aux)

        return Problem(H, W, R, Pb, Pr, B, [br, bc], np.array(grid))


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

    p.place_router([5, 5])
    print(p)
    print(p.score())
    # plot(p)
