import random

from grid import *
from solution import *


class Problem:
    def __init__(self, H, W, R, Pb, Pr, B, b, grid) -> None:
        self.H = H          # Number of rows of the grid
        self.W = W          # Number of columns of the grid
        self.R = R          # Radius of a router range
        self.Pb = Pb        # Price of connecting one cell to the backbone
        self.Pr = Pr        # Price of one wireless router
        self.B = B          # Maximum budget
        self.b = b          # Backboard coordinates
        self.grid = grid    # Building grid cells
        self.solution = Solution()

    def neighbours1(self):
        """Move a router to an adjacent cell"""

        possible_directions = [
            (-1, 0),     # N
            (-1, 1),     # NE
            (0, 1),      # E
            (1, 1)       # SE
            (1, 0),      # S
            (1, -1),     # SW
            (0, -1),     # W
            (-1, -1),    # NW
        ]

        n = len(self.solution.routers)  # Total number of routers

        # Dictionary Key: Each router; Value: List of every direction that router can go
        permutations = {}

        for _ in range(n * 8):
            # Select a random router to move
            i = random.randrange(n)

            # Select the direction in which the router will be moved
            direction = random.choice(possible_directions)

            # Add the router to the dictionary so that each new state isn´t repeated
            if i not in permutations:
                permutations[i] = []

            # Check if a router has already been moved to all adjacent cells
            while len(permutations[i]) == 8:
                i = random.randrange(n)

            # Select a new direction, until we find a new one that hasn't been considered yet
            while direction in permutations[i]:
                direction = random.choice(possible_directions)

            neighbour = self.solution.copy()
            neighbour.routers[i] = (
                neighbour.routers[i][0] + direction[0], 
                neighbour.routers[i][1] + direction[1]
            )

            yield neighbour

    def neighbours2(self):
        """Move the cutoff"""

        n = len(self.solution.routers)   # Total number of routers
        i = random.choice([-1, 1])       # Cutoff displacement. Either move it to the left or the right

        while self.solution.cutoff + i > n or self.solution.cutoff + i < 0:
            i = random.choice([-1, 1])

        neighbour = self.solution.copy()
        neighbour.cutoff += i

        yield neighbour

    def neighbours(self):
        # TODO: Recalculate spanning tree and covered targets

        pass

    def hill_climbing(self):
        pass

    def hill_climbing_steepest_ascent(self):
        pass

    def simmulatead_annealing(self):
        pass
