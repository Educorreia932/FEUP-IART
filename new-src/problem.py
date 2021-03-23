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
    def __init__(self, H, W, R, Pb, Pr, B, b, grid) -> None:
        self.H = H            # Number of rows of the grid
        self.W = W            # Number of columns of the grid
        self.R = R            # Radius of a router range
        self.Pb = Pb          # Price of connecting one cell to the backbone
        self.Pr = Pr          # Price of one wireless router
        self.B = B            # Maximum budget
        self.b = b            # Backboard coordinates
        self.grid = grid      # Building grid cells
        self.solution = None

    def get_neighbour(self, n: int, id: int):
        """Given an operation ID, returns the corresponding neighbour after performing that operation"""

        # Move router
        if id > n - 2:
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
                return None
            
            # Check if position is valid (not wall and not void)
            if self.grid.cells[new_coords[0], new_coords[1]] in (CELL_TYPE["#"], CELL_TYPE["-"]):
                return None

            neighbour = Solution(None, self.solution) 
            neighbour.routers[router_index] = new_coords

            return neighbour

        # Move cutoff either to the left or to the right
        else:
            cutoff_displacement = -1 if (n - id) % 2 == 0 else 1
            displaced_cutoff = self.solution.cutoff + cutoff_displacement 

            if displaced_cutoff > n or displaced_cutoff < 0:
                return None

            neighbour = Solution(None, self.solution) 
            neighbour.cutoff += cutoff_displacement

            return neighbour

    def neighbours(self):
        """Generate all possible neighbours of a given state"""
        # TODO: Recalculate spanning tree and covered targets

        # Total number of possible neighbours
        n = len(self.solution.routers) * 8 + 2           

        # Generate a list with IDs corresponding to the different operations permutations we may perform to obtain new neighbours
        neighbour_ids = list(range(n))                   

        # Shuffle the list so that we obtain a random neighbour each time
        random.shuffle(neighbour_ids)    
 
        for id in neighbour_ids:
            neighbour = self.get_neighbour(n, id)

            if neighbour is not None:
                yield neighbour

    def hill_climbing(self):
        self.solution = Solution(self)

        while True:
            for neighbour in self.neighbours():
                if neighbour.evaluate() > self.solution.evaluate():
                    self.solution = neighbour

                    break

            else:
                return self.solution

    def hill_climbing_steepest_ascent(self):
        bestneighbour = self.solution;
        while True:
            for neighbour in self.neighbours():
                if neighbour.evaluate() > self.solution.evaluate():
                    bestneighbour = neighbour
                    continue

            else:
                return self.solution
        self.solution = bestneighbour
        return self.solution

    def simmulatead_annealing(self):
        pass
