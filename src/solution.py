import random

from grid import *
from graph import *


class Solution:
    def __init__(self, problem, parent_solution=None) -> None:
        if parent_solution == None:
            self.routers = []
            self.problem = problem

            # Generate initial solution

            for _ in range(problem.B // problem.Pr):
                i = random.randrange(problem.H)
                j = random.randrange(problem.W)

                while [i, j] in self.routers or problem.grid.cells[i, j] in (CELL_TYPE["#"], CELL_TYPE["-"]):
                    i = random.randrange(problem.H)
                    j = random.randrange(problem.W)

                self.routers.append([i, j])

            # Index from which we starting not counting the routers to the final solution
            self.cutoff = len(self.routers)
            self.covered_cells = 0              # Number of covered cells by wireless

            # Graph representing backbone that connects all routers
            # self.graph = Graph(self.routers)

        else:
            self.routers = parent_solution.routers.copy()
            self.problem = parent_solution.problem
            self.cutoff = parent_solution.cutoff
            self.covered_cells = parent_solution.covered_cells

    def evaluate(self) -> int:
        """Evaluate the current solution using the score function"""

        t = self.covered_cells
        B = self.problem.B
        N = self.calculate_mst_length()  # Number of cables TODO: Change later
        Pb = self.problem.Pb
        M = len(self.routers)
        Pr = self.problem.Pr

        return 1000 * t + (B - (N * Pb + M * Pr))

    def calculate_mst_length(self) -> None:
        self.graph = Graph(self.routers[:self.cutoff])
        self.graph.kruskal()
        return self.graph.get_mst_distance()

    def calculate_coverage(self) -> None:
        radius = self.problem.R
        H = self.problem.H
        W = self.problem.W

        for router in self.routers:
            self.covered_cells += self.problem.grid.router_coverage(router, radius, H, W)
