from cell import Cell


class State():
    def __init__(self, starter_backbone, grid):
        self.grid = grid

        self.placed_routers = set()
        self.covered_targets = set()
        self.placed_backbones = set()
        self.backboned_cells = set()
        self.placed_backbones.add(starter_backbone)

        self.backboned_cells.update(
            self.grid.generate_neighbours(starter_backbone))

    def place_router(self, coords, radius):
        self.placed_routers.add(coords)

        for i in range(coords[0] - radius, coords[0] + radius + 1):
            for j in range(coords[1] - radius, coords[1] + radius + 1):
                if self.grid.router_can_see(coords, (i, j)) and coords != (i, j):
                    self.covered_targets.add((i, j))

    def place_backbone(self, coords):
        self.placed_backbones.add(coords)
        self.backboned_cells.update(self.grid.generate_neighbours(coords))

    def get_placed_backbones_amount(self):
        return len(self.placed_backbones)

    def get_placed_routers_amount(self):
        return len(self.placed_routers)

    def get_covered_targets_amount(self):
        return len(self.covered_targets)

    def get_backboned_cells(self):
        return self.backboned_cells

    def __str__(self):
        result = ""

        for i in range(self.grid.h):
            for j in range(self.grid.w):
                if (i, j) in self.placed_routers:
                    result += "R "

                elif (i, j) in self.placed_backbones:
                    result += "b "

                elif (i, j) in self.covered_targets:
                    result += "c "
                else:
                    result += Cell.to_character(self.grid.get_cell((i, j))) + " "

            result += "\n"

        return result
