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

    def get_neighbour(self, id: int) -> Solution:
        """
        Given an operation ID, returns the corresponding neighbour after performing that operation.
        """

        # Move router
        if id >= 2:
            router_index = (id - 2) // 8 - 1
            direction_index = (id - 2) % 8

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
            cutoff_displacement = -1 if id == 0 else 1
            displaced_cutoff = self.solution.cutoff + cutoff_displacement

            if displaced_cutoff > len(self.solution.routers) or displaced_cutoff <= 0:
                return [None] * 3

            neighbour = Solution(None, self.solution)
            router = neighbour.routers[neighbour.cutoff - 1]
            neighbour.cutoff = displaced_cutoff

            operation = "ADD" if cutoff_displacement == 1 else "REMOVE"

            return neighbour, operation, (router)

    def neighbours(self) -> Solution:
        """
        Generate all possible neighbours of a given state.
        """

        # Total number of possible neighbours
        n = len(self.solution.routers) * 8 + 2

        # Generate a list with IDs corresponding to the different move operations permutations we may perform to obtain new neighbours
        neighbour_ids = list(range(2, n))

        # Shuffle the list so that we obtain a random neighbour each time
        random.shuffle(neighbour_ids)

        # Prepend the two operations that correspond to moving the cuttoff
        neighbour_ids = [0, 1] + neighbour_ids

        for id in neighbour_ids:
            neighbour, operation, args = self.get_neighbour(id)

            if neighbour is not None:
                yield neighbour, operation, args

    def hill_climbing(self) -> Solution:
        """
        Hill-climbing optimization technique.
        """
        
        self.solution = Solution(self)
        current_score = self.solution.evaluate()

        while True:
            for neighbour, operation, args in self.neighbours():
                neighbour.calculate_coverage(operation, args)
                neighbour_score = neighbour.evaluate()

                if neighbour_score > current_score:
                    self.solution = neighbour
                    current_score = neighbour_score

                    print(f"Current score: {current_score}")

                    break

            else:
                return self.solution

    def hill_climbing_steepest_ascent(self) -> Solution:
        """
        Hill-climbing steepest ascent optimization technique.
        """

        self.solution = Solution(self)
        current_score = self.solution.evaluate()

        while True:
            neigbourhood = [(neighbour, operation, args) for (neighbour, operation, args) in self.neighbours()]
            neigbourhood_size = len(neigbourhood)

            if len(neigbourhood_size ) == 0:
                return self.solution

            best_neighbour, operation, args = max(neigbourhood, key=lambda s: s[0].evaluate())
            best_neighbour.calculate_coverage(operation, args)
            neighbour_score = best_neighbour.evaluate()

            if neighbour_score > current_score:
                self.solution = best_neighbour
                current_score = neighbour_score

                print(f"Current score: {current_score} | Number of neighbours: {neigbourhood_size}")

            else:
                return self.solution

    def simulated_annealing(self) -> Solution:
        """
        Simulated Annealing optimization technique.
        """
        
        self.solution = Solution(self)
        current_score = self.solution.evaluate()

        T0 = 100000
        t = T0
        neighbours = self.neighbours()
        currentIteration = 1

        while t > 0.1:
            print(f"Current temperature: {t}")

            neighbour, operation, args = next(neighbours, (None, None, None))

            if neighbour == None:
                break

            neighbour.calculate_coverage(operation, args)
            neighbour_score = neighbour.evaluate()

            delta = current_score - neighbour_score

            if delta >= 0:
                self.solution = neighbour
                current_score = neighbour_score
                neighbours = self.neighbours()

            else:
                print(f"Delta: {delta} | t: {t} | Chance: {math.exp(delta / t)}")
                if math.exp(delta / t) > random.uniform(0, 1):
                    self.solution = neighbour
                    current_score = neighbour_score
                    neighbours = self.neighbours()

            # Taken from http://what-when-how.com/artificial-intelligence/a-comparison-of-cooling-schedules-for-simulated-annealing-artificial-intelligence/
            # t = T0 * 0.95 ** currentIteration                 # Exponential multiplicative cooling
            t = T0 / (1 + 10 * math.log(1 + currentIteration))  # Logarithmical multiplicative cooling
            # t = T0 / (1 + 0.1 * currentIteration)             # Linear multiplicative cooling 
            # t = T0 / (1 + 0.1 * currentIteration ** 2)        # Quadratic multiplicative cooling
            currentIteration += 1

        return self.solution

    def genetic_algorithm(self):
        """
        Genetic algorithm optimization technique.
        """

        current_iterations = 0
        current_population = self.generate_initial_solution(10)
        max_iterations = 100

        while current_iterations < max_iterations:
            new_population = []

            for _ in range(int(len(current_population) / 2)):
                x = current_population.pop()
                y = current_population.pop()
                child = self.crossover_1(x, y)

                if random.uniform(0, 1) < 0.2:
                    child = self.mutation(child)
                new_population.append(child)
                print("A")
            current_population = new_population
            random.shuffle(current_population)
            print("Shuffled population")

        return max(current_population, key=lambda elem: elem.evaluate())

    def crossover_1(self, parent1: Solution, parent2: Solution):
        """
        Single-point crossover considering physical position of routers.
        """
        
        # Get the y bounds of the router lists in which there are routers in either list
        min_y_pos = self.H
        max_y_pos = 0
        
        print("Parent1: ", parent1)
        print("Parent2: ", parent2)


        for i in range(len(parent1.routers)):
            min_y_pos = min(
                min_y_pos, parent1.routers[i][0])
            max_y_pos = max(
                max_y_pos, parent1.routers[i][0])

        for i in range(len(parent2.routers)):
            min_y_pos = min(
                min_y_pos, parent2.routers[i][0])
            max_y_pos = max(
                max_y_pos, parent2.routers[i][0])

        # Make a random cut between the 2, both included
        y_cut = random.randint(min_y_pos, max_y_pos)
        child = Solution(None, parent1)
        child_routers = []

        if random.randint(1, 2) == 1:
            for i in range(len(parent1.routers)):
                if(parent1.routers[i][0] >= y_cut):
                    child_routers.append(parent1.routers[i])
            for i in range(len(parent2.routers)):
                if(parent2.routers[i][0] <= y_cut):
                    child_routers.append(parent2.routers[i])
        else:
            for i in range(len(parent1.routers)):
                if(parent1.routers[i][0] <= y_cut):
                    child_routers.append(parent1.routers[i])
            for i in range(len(parent2.routers)):
                if(parent2.routers[i][0] >= y_cut):
                    child_routers.append(parent2.routers[i])
                    
        cutoff = 0

        if (random.choice([True, False])):
            cutoff = parent1.cutoff

        else:
            cutoff = parent2.cutoff

        cutoff = min(cutoff, len(child_routers))
        child.routers = child_routers
        child.cutoff = cutoff

        return child

    def crossover_2(self, parent1: Solution, parent2: Solution, min_y_cuts: int, max_y_cuts: int):
        """
        Same as crossover 1, but instead of splitting the parts of the map with routers once, we split it a random number between min_y_cuts and max_y_cuts times
        """
        
        # Get the y bounds of the router lists in which there are routers in either list
        min_y_pos = self.H
        max_y_pos = 0

        for i in range(len(parent1.routers)):
            min_y_pos = min(
                min_y_pos, parent1.routers[i][0], parent2.routers[i][0])
            max_y_pos = max(
                max_y_pos, parent1.routers[i][0], parent2.routers[i][0])

        # Make a random cut between the 2, both included
        y_cuts = []
        num_cuts = random.randint(min_y_cuts, max_y_cuts)
        
        #Get the position of each cut
        for i in range(num_cuts):
            cut_placement = random.randint(min_y_pos, max_y_pos)
            
            if(cut_placement in y_cuts):
                y_cuts.append(cut_placement)
        
        y_cuts = np.sort(y_cuts)
        y_cuts.append(max_y_pos + 1)

        previous_cut_y_pos = min_y_pos
        for current_cut_y_pos in y_cuts:
            if(random.randint(1, 2) == 1):
                if(parent1.routers[i][0] < current_cut_y_pos and parent1.routers[i][0] >= previous_cut_y_pos):
                    child_routers.append(parent1.routers[i])
            else:
                if(parent2.routers[i][0] < current_cut_y_pos and parent2.routers[i][0] >= previous_cut_y_pos):
                    child_routers.append(parent2.routers[i])
            previous_y_cut = i


        cutoff = 0

        if (random.choice(True, False)):
            cutoff = parent1.cutoff

        else:
            cutoff = parent2.cutoff

        cutoff = min(cutoff, len(child_routers))
        child.routers = child_routers
        child.cutoff = cutoff
        return child

    def mutation(self, solution: Solution):
        self.solution = solution
        result, _ = next(self.neighbours())
        result.calculate_coverage()
        return result

    def generate_initial_solution(self, size):
        return [Solution(self) for _ in range(size)]
