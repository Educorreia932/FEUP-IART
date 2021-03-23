import random

from grid import *

class Solution:
    def __init__(self) -> None:
        self.routers = []

        # Generate initial solution

        for _ in range(self.B // self.Pr):
            i = random.randrange(self.H)
            j = random.randrange(self.W)

            while [i, j] in self.routers or self.grid.cells[i, j] in (CELL_TYPE["#"], CELL_TYPE["-"]):
                i = random.randrange(self.H)
                j = random.randrange(self.W)

            self.routers.append([i, j])

        self.cutoff = len(self.routers)   # Index from which we starting not counting the routers to the final solution
        self.covered_cells = 0            # Number of covered cells by wireless
        