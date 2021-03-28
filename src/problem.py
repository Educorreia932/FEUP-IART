import random
import numpy as np
import math

from grid import *
from solution import *

possible_directions = [
    (-1, 0),     # N
    (-1, 1),     # NE
    (0, 1),      # E
    (1, 1),      # SE
    (1, 0),      # S
    (1, -1),     # SW
    (0, -1),     # W
    (-1, -1),    # NW
]


class Problem:
    """Class to represent the problem information and solve it using different types of algorithms"""

    def __init__(self, H, W, R, Pb, Pr, B, b, grid) -> None:
        self.H = H            # Number of rows of the grid
        self.W = W            # Number of columns of the grid
        self.R = R            # Radius of a router range
        self.Pb = Pb          # Price of connecting one cell to the backbone
        self.Pr = Pr          # Price of one wireless router
        self.B = B            # Maximum budget
        self.b = b            # Backboard coordinates
        self.grid = grid      # Building's grid cells
        self.grid.problem = self
        self.solution = None

    def get_neighbour(self, n: int, id: int) -> Solution:
        """Given an operation ID, returns the corresponding neighbour after performing that operation"""

        # Move router
        if id < n - 2:
            router_index = id // 8 - 1
            direction_index = id % 8

            direction = possible_directions[direction_index]
            router_to_move = self.solution.routers[router_index]

            new_coords = (
                router_to_move[0] + direction[0],
                router_to_move[1] + direction[1]
            )

            # Check if it's within bounds of map
            if new_coords[0] < 0 or new_coords[0] >= self.H or new_coords[1] < 0 or new_coords[1] >= self.W:
                return [None] * 3

            # Check if position is valid (not wall and not void)
            if self.grid.cells[new_coords[0], new_coords[1]] in (CELL_TYPE["#"], CELL_TYPE["-"]):
                return [None] * 3

            neighbour = Solution(None, self.solution)
            neighbour.routers[router_index] = new_coords

            operation = "MOVE"

            return neighbour, operation, (router_to_move, new_coords)

        # Move cutoff either to the left or to the right
        else:
            cutoff_displacement = -1 if (n - id) % 2 == 0 else 1
            displaced_cutoff = self.solution.cutoff + cutoff_displacement

            if displaced_cutoff > len(self.solution.routers) or displaced_cutoff <= 0:
                return [None] * 3

            neighbour = Solution(None, self.solution)
            print(len(neighbour.routers), neighbour.cutoff)
            router = neighbour.routers[neighbour.cutoff - 1]
            neighbour.cutoff = displaced_cutoff

            operation = "ADD" if cutoff_displacement == 1 else "REMOVE"

            return neighbour, operation, (router)

    def neighbours(self, solution) -> Solution:
        """Generate all possible neighbours of a given state"""

        # Total number of possible neighbours
        n = len(self.solution.routers) * 8 + 2

        # Generate a list with IDs corresponding to the different operations permutations we may perform to obtain new neighbours
        neighbour_ids = list(range(n))

        # Shuffle the list so that we obtain a random neighbour each time
        random.shuffle(neighbour_ids)

        for id in neighbour_ids:
            neighbour, operation, args = self.get_neighbour(n, id)

            if neighbour is not None:
                yield neighbour, operation, args

    def hill_climbing(self) -> Solution:
        self.solution = Solution(self)
        current_score = self.solution.evaluate()
        i = 100

        while i > 0:
            for neighbour, operation, args in self.neighbours():
                neighbour.calculate_coverage(operation, args)
                neighbour_score = neighbour.evaluate()

                if neighbour_score > current_score:
                    self.solution = neighbour
                    current_score = neighbour_score

                    if i % 10 == 0:
                        print("Current score:", current_score, "i:", i)

                    i -= 1

                    break

            else:
                return self.solution

        return self.solution

    def hill_climbing_steepest_ascent(self) -> Solution:
        self.solution = Solution(self)
        current_score = self.solution.evaluate()
        i = 100

        while i > 0:
            neigbourhood = [(neighbour, operation, args)
                            for (neighbour, operation, args) in self.neighbours()]

            if len(neigbourhood) == 0:
                return self.solution

            best_neighbour, operation, args = max(
                neigbourhood, key=lambda s: s[0].evaluate())
            best_neighbour.calculate_coverage(operation, args)
            neighbour_score = best_neighbour.evaluate()

            if neighbour_score > current_score:
                self.solution = best_neighbour
                current_score = neighbour_score

                print("Current score:", current_score, "i:", i)

                i -= 1

            else:
                return self.solution

        return self.solution

    def simulated_annealing(self) -> Solution:
        self.solution = Solution(self)
        current_score = self.solution.evaluate()

        t = 100000
        neighbours = self.neighbours()
        while t > 0.1:
            print(f"Current temperature: {t}")
            neighbour, operation, args = next(neighbours, (None, None, None))
            if neighbour == None:
                break

            neighbour.calculate_coverage(operation, args)
            neighbour_score = neighbour.evaluate()

            delta = current_score - neighbour_score
            # print("Delta: ", delta, "t: ", t)
            if delta >= 0:
                self.solution = neighbour
                current_score = neighbour_score
                neighbours = self.neighbours()
            else:
                if math.exp(delta / t) > random.uniform(0, 1):
                    self.solution = neighbour
                    current_score = neighbour_score
                    neighbours = self.neighbours()

            t *= 0.95

        return self.solution

    def genetic_algorithm(self, max_iterations, crossover_function, mutation_function):
        current_iterations = 0
        current_population = self.generate_initial_solution()
        while current_iterations < max_iterations:
            new_population = []
            for i in range(len(current_population)):
                x = current_population.pop()
                y = current_population.pop()
                child = self.crossover(x, y)
                if random.uniform(0, 1) < 0.2:
                    child = self.mutation(child)
                new_population.append(child)
            current_population = new_population
            random.shuffle(current_population)

        return max(current_population, key=lambda elem: elem.evaluate())

    def crossover(self, parent1: Solution, parent2: Solution):
        # Get the y bounds of the router lists in which there are routers in either list
        min_y_pos = self.H
        max_y_pos = 0
        for i in range(len(parent1.routers)):
            min_y_pos = min(min_y_pos, parent1.routers[i][0], parent2.routers[i][0])
            min_y_pos = max(max_y_pos, parent1.routers[i][0], parent2.routers[i][0])
        # Make a random cut between the 2, both included
        y_cut = random.randint(min_y_pos, max_y_pos)
        child = Solution(None, parent1)
        child_routers = []


        if(random.randint(1, 2) == 1):
            for i in range(len(parent1.routers)):
                if(parent1.routers[i][0] > y_cut):
                    self.child_routers.append(parent1.routers[i])
                if(parent2.routers[i][0] < y_cut):
                    self.child_routers.append(parent2.routers[i])
        else:
            for i in range(len(parent1.routers)):
                if(parent1.routers[i][0] < y_cut):
                    self.child_routers.append(parent1.routers[i])
                if(parent2.routers[i][0] > y_cut):
                    self.child_routers.append(parent2.routers[i])
        cutoff = 0
        if(random.randint(1, 2) == 1):
            cutoff = parent1.cutoff
        else:
            cutoff = parent2.cutoff
        cutoff = min(cutoff, len(child_routers))
        child.routers = child_routers
        child.cutoff = cutoff
        return child

    def mutation(self, solution: Solution):
        self.solution = solution
        return next(self.neighbours())

    def generate_initial_solution(self, size):
        return [Solution(self) for _ in range(size)]

