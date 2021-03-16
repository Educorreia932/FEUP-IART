import random
from math import exp

from cell import Cell
from grid import Grid
from state import State
from graph import Graph


class Problem:
    def __init__(self, H, W, R, Pb, Pr, budget, backbone, cells):
        self.R = R
        self.Pb = Pb
        self.Pr = Pr
        self.B = budget

        self.grid = Grid(H, W, cells)
        self.current_iteration = 0
        self.current_state = State(backbone, self.grid)
        self.current_score = self.score(self.current_state)

    def __str__(self):
        return self.grid.__str__()

    def generate_new_states(self):
        n = self.current_state.get_uncovered_targets_amount()

        uncovered_targets = list(self.current_state.uncovered_targets)
        for _ in range(n):
            coords = random.choice(uncovered_targets)
            uncovered_targets.remove(coords)

            new_state = State(None, None, self.current_state)
            new_state.place_router(coords, self.R)

            yield new_state

    def normal_hillclimb(self) -> State:
        while True:
            for state in self.generate_new_states():
                neighbour = state
                neighbour_score = self.score(neighbour)

                if neighbour_score > self.current_score:
                    break

            else:
                return self.current_state

            self.current_state = neighbour
            self.current_score = neighbour_score

    def hillclimb_steepest_ascent(self) -> State:
        while True:
            neighbour_states = list(self.generate_new_states())
            self.current_iteration += 1
            print("Current iteration: " + self.current_iteration)

            if len(neighbour_states) == 0:
                return self.current_state

            neighbour = max(neighbour_states, key=self.score)
            neighbour_score = self.score(neighbour)

            if neighbour_score <= self.current_score:
                return self.current_state

            self.current_state = neighbour
            self.current_score = neighbour_score

    def simulated_annealing(self, iter_per_temp):
        kmax = 100
        k = 0
        
        while k < kmax:
            m = 0
            neighbour_states = self.generate_new_states()

            while m < iter_per_temp:
                
                s = next(neighbour_states)
                n_score = self.score(s)
                while n_score == -1:
                    s = next(neighbour_states)
                    n_score = self.score(s)

                curr_score = self.score(self.current_state)

                print(n_score)
                print(curr_score)

                if n_score >= curr_score:
                    self.current_state = s
                else:
                    delta = n_score - curr_score
                    print("Delta: " + str(delta) + "  Denominator: " + str(((k+1)/kmax))  + "\n")
                    if random.uniform(0.0, 1.0) < exp(- delta / ((k+1)/kmax)):
                        self.current_state = s
                m += 1
            k += 1

        return self.current_state

    def score(self, state) -> int:
        t = state.get_covered_targets_amount()
        N = state.get_placed_cables_amount()
        M = state.get_placed_routers_amount()

        budget = self.B - (N * self.Pb + M * self.Pr)

        if budget < 0:
            return -1

        return 1000 * t + budget
