import numpy as np

CELL_TYPE = {
    "-": -1,
    "#": 0,
    ".": 1
}

class Grid:
    def __init__(self, cells) -> None:
        self.cells = cells

    def router_can_see(self, r_coords, target) -> bool:
        """Returns wheter a route can see a cell or not"""

        top = min(target[0], r_coords[0])
        bottom = max(target[0], r_coords[0])

        left = min(target[1], r_coords[1])
        right = max(target[1], r_coords[1])

        return np.all(self.cells[top:bottom + 1, left:right + 1] != 0)
