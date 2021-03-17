import numpy as np

from graph import Graph

cells = {
    "BACKBONE": -2,
    "VOID": -1,
    "WALL": 0,
    "TARGET": 1,
    "ROUTER": 2,
    "CONNECTED_ROUTER": 3,
    "CABLE": 4
}

class State:
    def __init__(self, starter_backbone, grid, parent_state=None):
        if parent_state == None:
            self.grid = grid
            self.starter_backbone = starter_backbone
            self.targets = set(tuple(coords) for coords in np.argwhere(grid.cells == cells["TARGET"]))
            self.uncovered_targets = self.targets.copy()
            self.placed_routers = {starter_backbone}
            self.placed_cables = set()
            self.graph = None
            self.cable_amount = 1

        else:
            self.grid = parent_state.grid
            self.targets = parent_state.targets.copy()
            self.uncovered_targets = parent_state.uncovered_targets.copy()
            self.placed_routers = parent_state.placed_routers.copy()
            self.placed_cables = parent_state.placed_cables.copy()
            self.starter_backbone = parent_state.starter_backbone
            self.graph = parent_state.graph

            # Must be 1 because we are summing MST amount
            self.cable_amount = 1

    def place_router(self, coords, radius):
        self.placed_routers.add(coords)

        top = max(0, coords[0] - radius)
        bottom = min(self.grid.H, coords[0] + radius + 1)
        left = max(0, coords[1] - radius)
        right = min(self.grid.W, coords[1] + radius + 1)

        if coords in self.uncovered_targets:
            self.targets.remove(coords)
            self.uncovered_targets.remove(coords)

        for i in range(top, bottom):
            for j in range(left, right):
                if self.grid.get_cell((i, j)) != cells["VOID"] and self.grid.router_can_see(coords, (i, j)):
                    if (i, j) in self.uncovered_targets:
                        self.targets.remove((i, j))
                        self.uncovered_targets.remove((i, j))

        if self.graph == None:
            self.graph = Graph(self.placed_routers)

        else:
            self.graph = Graph([coords], self.graph)

        self.graph.kruskal()

        self.cable_amount += self.graph.get_mst_distance()

    def place_cell(self, coords):
        self.placed_cables.add(coords)

    def get_placed_cables_amount(self):
        return self.cable_amount

    def get_placed_routers_amount(self):
        return len(self.placed_routers)

    def get_covered_targets_amount(self):
        return self.grid.get_target_amount() - len(self.uncovered_targets)

    def get_targets_amount(self):
        return len(self.targets)

    def get_uncovered_targets_amount(self):
        return len(self.uncovered_targets)

    def wireless_coverage(self):
        """Returns an array with wireless coverage and updates cells"""

        result = np.zeros(self.grid.cells.shape, dtype=bool)

        for target in self.grid.target_cells - self.uncovered_targets:
            result[target] = True

        for router in self.placed_routers:
            i = router[0]
            j = router[1]

            self.grid.cells[i, j] = cells["ROUTER"]

        for cable in self.placed_cables:
            i = cable[0]
            j = cable[1]

            self.grid.cells[i, j] = cells["CABLE"]

        return result

    def backbone(self):
        result = np.zeros(self.grid.cells.shape, dtype=bool)

        g = Graph(self.placed_routers)
        g.kruskal()

        self.cable_amount = g.get_mst_distance()

        for router in g.result:
            start = g.vertices[router[0]]
            target = g.vertices[router[1]]

            if start[0] == target[0]:
                s = min((start[1], target[1]))
                e = max((start[1], target[1]))

                for j in range(s, e):
                    if j != start[1]:
                        self.placed_cables.add((start[0], j))

            elif start[1] == target[1]:
                s = min((start[0], target[0]))
                e = max((start[0], target[0]))
                for i in range(s, e):
                    if i != start[0]:
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

                    if current_cell == target:
                        break

                    else:
                        self.placed_cables.add(current_cell)

                if current_cell != target:
                    if current_cell[0] == target[0]:
                        s = min((current_cell[1], target[1]))
                        e = max((current_cell[1], target[1]))

                        for j in range(s, e):
                            if j != s:
                                self.placed_cables.add((current_cell[0], j))

                    if current_cell[1] == target[1]:
                        s = min((current_cell[0], target[0]))
                        e = max((current_cell[0], target[0]))

                        for i in range(s, e):
                            if i != s:
                                self.placed_cables.add((i, current_cell[1]))

        self.grid.cells[self.starter_backbone[0]][self.starter_backbone[1]] = cells["BACKBONE"]

        return result
