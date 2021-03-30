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

            # Number of covered cells by wireless
            self.covered_cells = 0

            self.calculate_initial_coverage()

            score = self.evaluate()

            while score < 0:
                removed_router = self.routers[self.cutoff - 1]
                self.cutoff -= 1
                self.calculate_coverage_after_operation(removed_router, -1)
                score = self.evaluate()

        else:
            self.routers = parent_solution.routers.copy()
            self.problem = parent_solution.problem
            self.cutoff = parent_solution.cutoff
            self.covered_cells = parent_solution.covered_cells
            self.coverage = parent_solution.coverage.copy()

    def evaluate(self) -> int:
        """
        Evaluate the current solution using the score function.
        """

        t = self.covered_cells
        B = self.problem.B
        N = self.calculate_mst()  
        Pb = self.problem.Pb
        M = self.cutoff
        Pr = self.problem.Pr

        remaining_budget = (B - (N * Pb + M * Pr))

        # print(f"Placed routers {M} | Remaining budget {remaining_budget}")

        if remaining_budget < 0:
            return -1

        return 1000 * t + remaining_budget

    def calculate_mst(self) -> None:
        """
        Calculate the graph (minimum spanning tree) representing backbone that connects all routers.
        """

        self.graph = Graph(self.routers[:self.cutoff] + [self.problem.b])
        self.graph.kruskal()

        return self.graph.get_mst_distance()

    def calculate_initial_coverage(self) -> None:
        H = self.problem.H
        W = self.problem.W

        self.coverage = np.zeros((H, W), dtype=np.int8)

        for router in self.routers[:self.cutoff]:
            self.calculate_coverage_after_operation(router, 1)

    def calculate_coverage(self, operation: str, args) -> None:
        """
        Calculate the coverage of the cells after performing an operation.
        """

        if operation == "MOVE":
            old_coords = args[0]
            new_coords = args[1]

            self.calculate_coverage_after_operation(old_coords, -1)
            self.calculate_coverage_after_operation(new_coords, 1)

        elif operation == "ADD":
            router_to_add = args

            self.calculate_coverage_after_operation(router_to_add, 1)

        elif operation == "REMOVE":
            router_to_remove = args

            self.calculate_coverage_after_operation(router_to_remove, -1)

    def calculate_coverage_after_operation(self, router, operation: int) -> None:
        """
        Calculate the resulting coverage after removing or adding a router.
        """
        router_covered_cells = self.problem.grid.router_coverage(router)

        for cell in router_covered_cells:
            before = self.coverage[cell[0], cell[1]] 
            self.coverage[cell[0], cell[1]] = max(0, before + operation)
            after = self.coverage[cell[0], cell[1]]
            
            if before == 0 and after == 1:
                self.covered_cells += 1

            elif before == 1 and after == 0:
                self.covered_cells -= 1

    def get_placed_routers(self) -> list:
        """
        Returns the effectively placed routers, that is, those not being cut off.
        """
        return self.routers[:self.cutoff]
