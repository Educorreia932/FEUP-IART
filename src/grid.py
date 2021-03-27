import numpy as np

CELL_TYPE = {
    "-": -1,
    "#": 0,
    ".": 1
}

class Grid:
    def __init__(self, cells) -> None:
        self.cells = cells
        print("Target amount:", len(np.argwhere(self.cells == CELL_TYPE["."])))

    def router_can_see(self, coordinates, target) -> bool:
        """Returns wheter a route can see a cell or not"""

        top = min(target[0], coordinates[0])
        bottom = max(target[0], coordinates[0])

        left = min(target[1], coordinates[1])
        right = max(target[1], coordinates[1])

        return np.all(self.cells[top:bottom + 1, left:right + 1] != 0)

    def router_coverage(self, coordinates) -> bool:
        """Returns the cells covered by a router's wireless range"""

        radius = self.problem.R
        H = self.problem.H
        W = self.problem.W

        covered_cells = []

        top = max(coordinates[0] - radius, 0) # Y position of topmost tile checked for coverage

        for i in range(coordinates[0], top - 1, -1):
            if self.cells[i, coordinates[1]] == CELL_TYPE["#"]:
                top = i
                break
                
        bottom = min(coordinates[0] + radius, H - 1) # Y position of bottommost tile checked for coverage

        for i in range(coordinates[0] + 1, bottom + 1):
            if self.cells[i, coordinates[1]] == CELL_TYPE["#"]:
                bottom = i
                break

        left = max(coordinates[1] - radius, 0)

        for i in range(coordinates[1] - 1, left - 1, -1):
            if self.cells[coordinates[0], i] == CELL_TYPE["#"]:
                left = i
                break

        right = min(coordinates[1] + radius, W - 1)

        for i in range(coordinates[1] + 1, right + 1):
            if self.cells[coordinates[0], i] == CELL_TYPE["#"]:
                right = i
                break

        for i in range(top, bottom):
            for j in range(left, right):
                target = (i, j)

                if self.router_can_see(coordinates, target):
                    covered_cells.append(coordinates)

        return covered_cells
