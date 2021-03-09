from cell import Cell


class State():

    def __init__(self, starter_backbone, board):
        self.board = board

        self.placed_routers = set()
        self.covered_targets = set()
        self.placed_backbones = set()
        self.backboned_cells = set()
        self.placed_backbones.add(starter_backbone)

        self.backboned_cells.update(
            self.board.generate_neighbours(starter_backbone))

    def place_router(self, coords):
        placed_routers.add(coords)
        for i in range(coords[0] - self.radius, coords[0] + self.radius + 1):
            for j in range(coords[1] - self.radius, coords[1] + self.radius + 1):
                if self.router_can_see(coords, (i, j)) and coords != (i, j):
                    self.covered_targets.add((i, j))

    def place_backbone(self, coords):
        placed_backbones.add(coords)
        self.backboned_cells.update(self.board.generate_neighbours(coords))

    def get_placed_backbones_amount(self):
        return len(self.placed_backbones)

    def get_placed_routers_amount(self):
        return len(self.placed_routers)

    def get_covered_targets_amount(self):
        return len(self.covered_targets)
