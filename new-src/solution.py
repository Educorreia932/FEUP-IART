import random

from grid import *

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

            self.cutoff = len(self.routers)   # Index from which we starting not counting the routers to the final solution
            self.covered_cells = 0            # Number of covered cells by wireless
        else:
            self.routers = parent_solution.routers.copy()
            self.problem = parent_solution.problem
            self.cutoff = parent_solution.cutoff
            self.covered_cells = parent_solution.covered_cells

    def evaluate(self):
        """Evaluate the current solution using the score function"""
        t = self.covered_cells 
        B = self.problem.B
        N = 0 # Number of cables TODO: Change later
        Pb = self.problem.Pb
        M = len(self.routers)
        Pr = self.problem.Pr

        return 1000 * t + (B - (N * Pb + M * Pr))
