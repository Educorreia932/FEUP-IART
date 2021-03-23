import numpy as np

CELL_TYPE = {
    "-": -1,
    "#": 0,
    ".": 1
}

class Grid:
    def __init__(self, cells) -> None:
        self.cells = cells

    def router_can_see(self, coordinates, target) -> bool:
        """Returns wheter a route can see a cell or not"""

        top = min(target[0], coordinates[0])
        bottom = max(target[0], coordinates[0])

        left = min(target[1], coordinates[1])
        right = max(target[1], coordinates[1])

        return np.all(self.cells[top:bottom + 1, left:right + 1] != 0)

    def router_coverage(self, coordinates, radius, H, W) -> bool:
        """Returns the number of cells covered by a router's wireless range"""

        covered_cells = 0

        top = min(coordinates[0] - radius, H)
        bottom = max(coordinates[0] + radius, H)

        left = min(coordinates[1] - radius, W)
        right = max(coordinates[1] + radius, W)

        for i in range(top, bottom):
            for j in range(left, right):
                target = (i, j)

                if self.router_can_see(coordinates, target):
                    covered_cells += 1

        return covered_cells
