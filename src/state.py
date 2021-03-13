import numpy as np

from cell import Cell
from graph import Graph


class State:
    def __init__(self, starter_backbone, grid, parent_state=None):

        if parent_state == None:
            self.grid = grid
            self.uncovered_targets = set(
                tuple(coords) for coords in np.argwhere(grid.cells == Cell.TARGET))
            self.placed_routers = set()
            # self.covered_targets = set()
            self.placed_cables = set()
            # self.backboned_cells = set()
            # self.placed_cables.add(starter_backbone)
            self.cable_amount = 1
            # self.backboned_cells.update(self.grid.generate_neighbours(starter_backbone))
        else:
            self.grid = parent_state.grid
            self.uncovered_targets = parent_state.uncovered_targets.copy()
            self.placed_routers = parent_state.placed_routers.copy()
            self.placed_cables = parent_state.placed_cables.copy()
            # Must be 1 because we are summing mst amount
            self.cable_amount = 1

    def place_router(self, coords, radius):
        self.placed_routers.add(coords)

        top = max(0, coords[0] - radius)
        bottom = min(self.grid.H, coords[0] + radius + 1)
        left = max(0, coords[1] - radius)
        right = min(self.grid.W, coords[1] + radius + 1)

        self.uncovered_targets.remove(coords)

        for i in range(top, bottom):
            for j in range(left, right):
                if self.grid.get_cell((i, j)) != Cell.VOID and self.grid.router_can_see(coords, (i, j)):
                    # self.covered_targets.add((i, j))

                    if (i, j) in self.uncovered_targets:
                        self.uncovered_targets.remove((i, j))

        g = Graph(self.placed_routers)
        g.kruskal()
        self.cable_amount += g.get_mst_distance()

    def place_cell(self, coords):
        self.placed_cables.add(coords)
        # self.backboned_cells.update(self.grid.generate_neighbours(coords))

    def get_placed_cables_amount(self):
        return self.cable_amount

    def get_placed_routers_amount(self):
        return len(self.placed_routers)

    def get_covered_targets_amount(self):
        return self.grid.get_target_amount() - len(self.uncovered_targets)

    def get_uncovered_targets_amount(self):
        return len(self.uncovered_targets)

    # def get_backboned_cells(self):
    #     return self.backboned_cells

    def wireless_coverage(self):
        """Returns an array with wireless coverage and updates cells"""

        result = np.zeros(self.grid.cells.shape, dtype=bool)

        for target in self.grid.target_cells - self.uncovered_targets:
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

    def backbone(self):

        result = np.zeros(self.grid.cells.shape, dtype=bool)

        g = Graph(self.placed_routers)
        g.kruskal()
        self.cable_amount = g.get_mst_distance()

        for router in g.vertices:

            start = router.get_coords()
            target = router.path.get_coords()

            if start[0] == target[0]:
                for j in range(start[1], target[1]):
                    if j != start[1]:
                        # result[start[0], j] = Cell.CABLE
                        self.placed_cables.add((start[0], j))
            elif start[1] == target[1]:
                for i in range(start[0], target[0]):
                    if i != start[0]:
                        # result[i, start[1]] = Cell.CABLE
                        self.placed_cables.add((i, start[1]))
            else:
                if (target[0] - start[0]) < 0:
                    xdiff = -1
                elif (target[0] - start[0]) > 0:
                    xdiff = 1
                else:
                    xdiff = 0

                if (target[1] - start[1]) < 0:
                    ydiff = -1
                elif (target[1] - start[1]) > 0:
                    ydiff = 1
                else:
                    ydiff = 0

                delta = (xdiff, ydiff)

                current_cell = (start[0], start[1])
                while current_cell[0] != target[0] and current_cell[1] != target[1]:

                    current_cell = (
                        current_cell[0] + delta[0], current_cell[1] + delta[1])
                    print(current_cell,  "     ", target)
                    if current_cell == target:
                        break
                    else:
                        # result[current_cell[0], current_cell[1]] = Cell.CABLE
                        self.placed_cables.add(current_cell)

                if current_cell != target:
                    
                    if current_cell[0] == target[0]:

                        start = min((current_cell[1], target[1]))
                        end = max((current_cell[1], target[1]))

                        for j in range(start, end):
                            if j != start:
                                # result[current_cell[0], j] = Cell.CABLE
                                self.placed_cables.add((current_cell[0], j))

                    if current_cell[1] == target[1]:

                        start = min((current_cell[0], target[0]))
                        end = max((current_cell[0], target[0]))

                        for i in range(start, end):
                            if i != start:
                                # result[i, current_cell[1]] = Cell.CABLE
                                self.placed_cables.add((i, current_cell[1]))

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
                    result += Cell.to_character(
                        self.grid.get_cell((i, j))) + " "

            result += "\n"

        return result
