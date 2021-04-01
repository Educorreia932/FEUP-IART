import random
import numpy as np
import math
from time import sleep

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

    def get_neighbour(self, id: int):
        """
        Given an operation ID, returns the corresponding neighbour after performing that operation.
        """

        # Move router
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
            return [None] * 2

        # Check if position is valid (not wall and not void)
        while self.grid.cells[new_coords[0], new_coords[1]] in (CELL_TYPE["#"], CELL_TYPE["-"]):
            new_coords = (
                new_coords[0] + direction[0],
                new_coords[1] + direction[1]
            )

            # Check if it's within bounds of map
            if new_coords[0] < 0 or new_coords[0] >= self.H or new_coords[1] < 0 or new_coords[1] >= self.W:
                return [None] * 2

        neighbour = Solution(None, self.solution)
        neighbour.routers[router_index] = new_coords

        return neighbour, [router_to_move, new_coords]

    def neighbours(self):
        """
        Generate all possible neighbours of a given state.
        """

        # Total number of possible neighbours
        n = len(self.solution.routers) * 8

        # Generate a list with IDs corresponding to the different operations permutations we may perform to obtain new neighbours
        neighbour_ids = list(range(n))

        # Shuffle the list so that we obtain a random neighbour each time
        random.shuffle(neighbour_ids)

        for id in neighbour_ids:
            neighbour, args = self.get_neighbour(id)

            if neighbour is not None:
                yield neighbour, args

    def hill_climbing(self) -> Solution:
        """
        Hill-climbing optimization technique.
        """
        
        self.solution = Solution(self)
        current_score = self.solution.evaluate()
        i = 0

        while i < 50:
            for neighbour, args in self.neighbours():
                neighbour.update_coverage(args)
                neighbour.calculate_graph()

                neighbour_score = neighbour.evaluate()

                if neighbour_score > current_score:
                    self.solution = neighbour
                    current_score = neighbour_score

                    print(f"Current score: {current_score}")
                    i += 1

                    break

            else:
                return self.solution

        return self.solution

    def hill_climbing_steepest_ascent(self) -> Solution:
        """
        Hill-climbing steepest ascent optimization technique.
        """

        self.solution = Solution(self)
        neighbour_score = self.solution.evaluate()
        best_neighbour_score = neighbour_score 

        while True:
            improved = False

            for (neighbour, args) in self.neighbours():
                neighbour.update_coverage(args)
                neighbour.calculate_graph()
                neighbour_score = neighbour.evaluate()

                if neighbour_score > best_neighbour_score:
                    self.solution = neighbour
                    best_neighbour_score = neighbour_score
                    improved = True

            if not improved:
                return self.solution

    def simulated_annealing(self) -> Solution:
        """
        Simulated Annealing optimization technique.
        """

        self.solution = Solution(self)
        current_score = self.solution.evaluate()
        best_solution = self.solution
        best_score = current_score

        T0 = 100000
        t = T0
        iterations_per_temperature = 3
        neighbours = self.neighbours()
        currentIteration = 1

        while t > 10:
            print(f"Current temperature: {t}")

            for _ in range(iterations_per_temperature):
                neighbour, args = next(neighbours, (None, None))
                # print("args: ", args)
                if neighbour == None:
                    break

                
                neighbour.calculate_coverage(args)
                neighbour_score = neighbour.evaluate()
                if neighbour_score != -1:
                    delta = current_score - neighbour_score

                    if delta >= 0:
                        self.solution = neighbour
                        current_score = neighbour_score
                        if neighbour_score > best_score:
                            best_solution = self.solution
                            best_score = current_score 
                        neighbours = self.neighbours()

                    else:
                        print(f"Delta: {delta} | t: {t} | Chance: {math.exp(delta / t)}")
                        if math.exp(delta / t) > random.uniform(0, 1):
                            self.solution = neighbour
                            current_score = neighbour_score
                            if neighbour_score > best_score:
                                best_solution = self.solution
                                best_score = current_score
                            neighbours = self.neighbours()

            # Taken from http://what-when-how.com/artificial-intelligence/a-comparison-of-cooling-schedules-for-simulated-annealing-artificial-intelligence/
            t = T0 * 0.95 ** currentIteration                 # Exponential multiplicative cooling
            # t = T0 / (1 + 100 * math.log(1 + currentIteration))  # Logarithmical multiplicative cooling
            # t = T0 / (1 + 10 * currentIteration)             # Linear multiplicative cooling 
            # t = T0 / (1 + 0.1 * currentIteration ** 2)        # Quadratic multiplicative cooling

            # beta = (1 / (self.R * 1000))
            # t = t / (1 + beta * t)                                            # Taken from https://link.springer.com/referenceworkentry/10.1007%2F978-3-540-92910-9_49
            currentIteration += 1
            print(f"Current temperature: {t}")


        return best_solution

    def genetic_algorithm(self):
        """
        Genetic algorithm optimization technique.
        """

        current_iterations = 0
        current_population = self.generate_initial_solution(8)
        max_iterations = 20

        while current_iterations < max_iterations:
            new_population = []


            for _ in range(int(len(current_population))):
                x = current_population[random.randint(0, int(len(current_population) / 2))]
                y = current_population[random.randint(0, int(len(current_population) / 2))]
                child = self.crossover_1(x, y)

                if random.uniform(0, 1) < 0.2:
                    child = self.mutation(child)
                child.calculate_initial_coverage()
                new_population.append(child)

            current_population = new_population
            current_population.sort(reverse=True, key=lambda elem: elem.evaluate())
            current_iterations += 1

        return max(current_population, key=lambda elem: elem.evaluate())

    def crossover_1(self, parent1: Solution, parent2: Solution):
        """
        Single-point crossover considering physical position of routers.
        """
        
        # Get the y bounds of the router lists in which there are routers in either list
        min_y_pos = self.H
        max_y_pos = 0

        #Get the y positions of the bottom and topmost routers
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
                min_y_pos, parent1.routers[i][0])
            max_y_pos = max(
                max_y_pos, parent1.routers[i][0])

        for i in range(len(parent2.routers)):
            min_y_pos = min(
                min_y_pos, parent2.routers[i][0])
            max_y_pos = max(
                max_y_pos, parent2.routers[i][0])



        # Make a random cut between the 2, both included
        y_cuts = []
        num_cuts = random.randint(min_y_cuts, max_y_cuts)
        
        #Get the position of each cut
        for i in range(num_cuts):
            cut_placement = random.randint(min_y_pos, max_y_pos)
            if(cut_placement not in y_cuts):
                y_cuts.append(cut_placement)
            else:
                i -= 1
        
        y_cuts = np.sort(y_cuts)
        y_cuts.append(max_y_pos + 1)

        
        child = Solution(None, parent1)
        child_routers = []


        previous_cut_y_pos = min_y_pos
        for current_cut_y_pos in y_cuts:
            if(random.randint(1, 2) == 1):
                for i in range(len(parent1.routers)):
                    if(parent1.routers[i][0] < current_cut_y_pos and parent1.routers[i][0] >= previous_cut_y_pos):
                        child_routers.append(parent1.routers[i])
            else:
                for i in range(len(parent2.routers)):
                    if(parent2.routers[i][0] < current_cut_y_pos and parent2.routers[i][0] >= previous_cut_y_pos):
                        child_routers.append(parent2.routers[i])
            previous_cut_y_pos = current_cut_y_pos


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
        return next(self.neighbours())[0]

    def generate_initial_solution(self, size):
        return [Solution(self) for _ in range(size)]
