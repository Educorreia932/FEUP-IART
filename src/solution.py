import random

from grid import *
from graph import *


class Solution:
    def __init__(self, problem, parent_solution=None) -> None:
        if parent_solution == None:
            self.routers = []
            self.problem = problem

            # Generate initial solution
            print("Generating initial solution...")

            for _ in range(problem.B // problem.Pr):
                i = random.randrange(problem.H)
                j = random.randrange(problem.W)

                while [i, j] in self.routers or problem.grid.cells[i, j] in (CELL_TYPE["#"], CELL_TYPE["-"]):
                    i = random.randrange(problem.H)
                    j = random.randrange(problem.W)

                self.routers.append((i, j))

            # Index from which we starting not counting the routers to the final solution
            self.cutoff = len(self.routers)

            # Number of covered cells by wireless
            self.covered_cells = 0

            self.calculate_coverage()
            self.calculate_graph()

            score = self.evaluate()

            while score < 0:
                removed_router = self.routers[self.cutoff - 1]
                self.cutoff -= 1
                self.update_coverage_after_operation(removed_router, -1)
                score = self.evaluate()

            print("Finished generating")

        else:
            self.routers = parent_solution.routers.copy()
            self.problem = parent_solution.problem
            self.cutoff = parent_solution.cutoff
            self.covered_cells = parent_solution.covered_cells
            self.coverage = parent_solution.coverage.copy()
            self.graph = Graph(parent_graph=parent_solution.graph)

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

        while remaining_budget < 0:
            # Reduce cuttoff for as long as we must until the solution is feasible
            # That is, until the remaining budget is positive

            self.reduce_cuttoff()    # Update the cutoff index, the coverage and the graph
            t = self.covered_cells
            M = self.cutoff
            N = self.calculate_mst()

            remaining_budget = (B - (N * Pb + M * Pr))

        # print(f"Placed routers {M} | Remaining budget {remaining_budget}")

        return 1000 * t + remaining_budget

    def calculate_mst(self) -> None:
        """
        Calculate the graph (minimum spanning tree) representing backbone that connects all routers.
        """
        
        self.graph.kruskal()

        return self.graph.get_mst_distance()

    def calculate_graph(self):
        self.graph = Graph(self.get_placed_routers() + [self.problem.b])

    def update_graph_after_move(self, before, after):
        self.graph = Graph(parent_graph=self.graph)
        self.graph.moved_router(before, after)

    def update_graph_after_add(self, router):
        self.graph = Graph(parent_graph=self.graph)
        self.graph.removed_router(router)

    def update_graph_after_remove(self, router):
        self.graph = Graph(parent_graph=self.graph)
        self.graph.removed_router(router)

    def calculate_coverage(self) -> None:
        H = self.problem.H
        W = self.problem.W

        self.coverage = np.zeros((H, W), dtype=np.int8)
        self.covered_cells = 0

        for router in self.routers[:self.cutoff]:
            self.update_coverage_after_operation(router, 1)

    def update_coverage(self, coordinates) -> None:
        """
        Calculate the coverage of the cells after performing moving a router.
        """

        old_coords = coordinates[0]
        new_coords = coordinates[1]

        self.update_coverage_after_operation(old_coords, -1)
        self.update_coverage_after_operation(new_coords, 1)

    def update_coverage_after_operation(self, router, operation: int) -> None:
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

    def reduce_cuttoff(self) -> None:
        """
        Reduce the cutoff, effectively removing the last router from the solution
        """

        removed_router = self.routers[self.cutoff - 1]
        self.cutoff -= 1

        self.update_coverage_after_operation(removed_router, -1)
        self.update_graph_after_remove(removed_router)

    def increase_cuttoff(self) -> None:
        """
        Increase the cutoff, effectively adding the last router to the solution
        """

        added_router = self.routers[self.cutoff - 1]
        self.cutoff += 1

        self.update_coverage_after_operation(added_router, 1)
        self.update_graph_after_add()
