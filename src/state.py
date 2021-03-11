import numpy as np

from cell import Cell


class State:
    def __init__(self, starter_backbone, grid):
        self.grid = grid

        self.uncovered_targets = set(tuple(coords) for coords in np.argwhere(grid.cells == Cell.TARGET))

        self.placed_routers = set()
        self.covered_targets = set()
        self.placed_cables = set()
        self.backboned_cells = set()
        self.placed_cables.add(starter_backbone)
        self.backboned_cells.update(self.grid.generate_neighbours(starter_backbone))


    def place_router(self, coords, radius):
        self.placed_routers.add(coords)

        top = max(0, coords[0] - radius)
        bottom = min(self.grid.H, coords[0] + radius + 1)
        left = max(0, coords[1] - radius)
        right = min(self.grid.W, coords[1] + radius + 1)

        self.uncovered_targets.remove(coords)

        for i in range(top, bottom):
            for j in range(left, right):
                if self.grid.router_can_see(coords, (i, j)) and self.grid.get_cell((i, j)) != Cell.VOID:
                    self.covered_targets.add((i, j))

                    if (i, j) in self.uncovered_targets:
                        self.uncovered_targets.remove((i, j))

    def place_cell(self, coords):
        self.placed_cables.add(coords)
        self.backboned_cells.update(self.grid.generate_neighbours(coords))

    def get_placed_cables_amount(self):
        return len(self.placed_cables)

    def get_placed_routers_amount(self):
        return len(self.placed_routers)

    def get_covered_targets_amount(self):
        return len(self.covered_targets)

    def get_uncovered_targets_amount(self):
        return len(self.uncovered_targets)

    def get_backboned_cells(self):
        return self.backboned_cells

    def wireless_coverage(self):
        """Returns an array with wireless coverage and updates cells"""

        result = np.zeros(self.grid.cells.shape, dtype=bool)

        for target in self.covered_targets:
            result[target] = True

        for router in self.placed_routers:
            i = router[0]
            j = router[1]

            self.grid.cells[i, j] = Cell.ROUTER

        for cable in self.placed_cables:
            i = cable[0]
            j = cable[1]

            self.grid.cells[i, j] = Cell.CABLE

        return result

    def __str__(self):
        result = ""

        for i in range(self.grid.H):
            for j in range(self.grid.W):
                if (i, j) in self.placed_routers:
                    result += "R "

                elif (i, j) in self.placed_cables:
                    result += "b "

                elif (i, j) in self.covered_targets:
                    result += "c "

                else:
                    result += Cell.to_character(self.grid.get_cell((i, j))) + " "

            result += "\n"

        return result
