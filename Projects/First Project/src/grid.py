import numpy as np

"""
Possible cell types
"""

CELL_TYPE = {
    "-": -1,  # Void cell
    "#": 0,   # Wall cell
    ".": 1,   # Target cell
    "r": 2,   # Router cell
    "b": 3,   # Backbone cell
    "c": 4    # Cable cell
}


class Grid:
    """
    Class to represent the problem's building grid as a NumPy array.
    """

    def __init__(self, cells: np.array) -> None:
        self.cells = cells

    def router_can_see(self, coordinates, target) -> bool:
        """
        Returns wheter a route can see a cell or not.
        """

        top = min(target[0], coordinates[0])
        bottom = max(target[0], coordinates[0])

        left = min(target[1], coordinates[1])
        right = max(target[1], coordinates[1])

        return np.all(self.cells[top:bottom + 1, left:right + 1] != CELL_TYPE["#"])

    def router_coverage(self, coordinates) -> bool:
        """
        Returns the cells covered by a router's wireless range
        """

        radius = self.problem.R
        H = self.problem.H
        W = self.problem.W

        covered_cells = []

        # Y position of topmost tile checked for coverage
        top = max(coordinates[0] - radius, 0)

        for i in range(coordinates[0], top - 1, -1):
            if self.cells[i, coordinates[1]] == CELL_TYPE["#"]:
                top = i
                break

        # Y position of bottommost tile checked for coverage
        bottom = min(coordinates[0] + radius + 1, H)

        for i in range(coordinates[0] + 1, bottom + 1):
            if self.cells[i, coordinates[1]] == CELL_TYPE["#"]:
                bottom = i
                break

        left = max(coordinates[1] - radius, 0)

        for i in range(coordinates[1] - 1, left - 1, -1):
            if self.cells[coordinates[0], i] == CELL_TYPE["#"]:
                left = i
                break

        right = min(coordinates[1] + radius + 1, W)

        for i in range(coordinates[1] + 1, right + 1):
            if self.cells[coordinates[0], i] == CELL_TYPE["#"]:
                right = i
                break

        for i in range(top, bottom):
            for j in range(left, right):
                target = (i, j)

                if self.cells[target] == CELL_TYPE["."] and self.router_can_see(coordinates, target):
                    covered_cells.append(target)

        return covered_cells

    def place_router(self, coords):
        """
        Places a router cell.
        """

        self.cells[coords[0], coords[1]] = CELL_TYPE["r"]

    def place_backbone(self, coords):
        """
        Places the initial backbone cell.
        """

        self.cells[coords[0], coords[1]] = CELL_TYPE["b"]

    def place_cable(self, coords):
        """
        Places a cable cell.
        """
        
        self.cells[coords[0], coords[1]] = CELL_TYPE["c"]
