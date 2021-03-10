import numpy as np

from cell import Cell


class Grid:
    def __init__(self, H, W, cells):
        self.H = H
        self.W = W
        self.cells = cells

    def get_cell(self, coords):
        return self.cells[coords[0], coords[1]]

    def generate_neighbours(self, coords):
        """Generates neighbours of coords"""

        return [
            (coords[0] + i, coords[1] + j) for i in [-1, 0, 1]
            for j in [-1, 0, 1] if
            0 <= i + coords[0] < self.H and
            0 <= j + coords[1] < self.W and
            i + coords[0] != j + coords[1] and
            self.cells[i + coords[0]][j + coords[1]] != Cell.WALL
        ]

    def router_can_see(self, r_coords, target):
        """Returns wheter a route can see a cell or not."""

        top = min(target[0], r_coords[0])
        bottom = max(target[0], r_coords[0])

        left = min(target[1], r_coords[1])
        right = max(target[1], r_coords[1])

        return np.all(self.cells[top:bottom + 1, left:right + 1] != Cell.WALL)

    def __str__(self):
        result = ""

        for line in self.cells:
            for elem in line:
                result += Cell.to_character(elem) + " "

            result += "\n"

        return result
