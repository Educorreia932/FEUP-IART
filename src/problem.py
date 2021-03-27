import random
import numpy as np

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

            if displaced_cutoff > n or displaced_cutoff < 0:
                return [None] * 3

            neighbour = Solution(None, self.solution) 
            router = neighbour.routers[neighbour.cutoff - 1]
            neighbour.cutoff = displaced_cutoff

            operation = "ADD" if cutoff_displacement == 1 else "REMOVE"

            return neighbour, operation, (router)

    def neighbours(self) -> Solution:
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

    def hill_climbing(self):
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

    def hill_climbing_steepest_ascent(self):
        best_neighbour = self.solution

        while True:
            for neighbour in self.neighbours():
                if neighbour.evaluate() > self.solution.evaluate():
                    best_neighbour = neighbour
                    continue

            else:
                return self.solution

    def simmulatead_annealing(self):
        pass
