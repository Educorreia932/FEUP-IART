import random
from math import exp

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
        n = self.current_state.get_targets_amount()
        targets = list(self.current_state.targets)

        for _ in range(n):
            i = random.randrange(n)
            coords = targets[i]
            targets.pop(i)
            n -= 1

            new_state = State(None, None, self.current_state)
            new_state.place_router(coords, self.R)

            yield new_state

    def normal_hillclimb(self) -> State:
        while self.budget_left(self.current_state) > self.Pr:
            print("Targets left: ", self.current_state.get_uncovered_targets_amount(), " - Budget: ", self.current_score)

            for state in self.generate_new_states():
                neighbour = state
                neighbour_score = self.score(neighbour)

                if neighbour_score > self.current_score:
                    break

            else:
                return self.current_state

            self.current_state = neighbour
            self.current_score = neighbour_score

        return self.current_state

    def hillclimb_steepest_ascent(self) -> State:
        while self.budget_left(self.current_state) > self.Pr:
            print(self.current_state.get_uncovered_targets_amount())

            neighbour_states = list(self.generate_new_states())
            self.current_iteration += 1
            print("Current iteration: " + str(self.current_iteration))

            if len(neighbour_states) == 0:
                return self.current_state

            neighbour = max(neighbour_states, key=self.score)
            neighbour_score = self.score(neighbour)

            if neighbour_score <= self.current_score:
                return self.current_state

            self.current_state = neighbour
            self.current_score = neighbour_score

    def simulated_annealing(self):
        T = 100000
        
        while self.budget_left(self.current_state) > self.Pr:
            T -= 100
            if T <= 0:
                return self.current_state

            neighbour_states = self.generate_new_states()

            try:
                s = next(neighbour_states)
                n_score = self.score(s)
                while n_score == -1:
                    s = next(neighbour_states)
                    n_score = self.score(s)
            except StopIteration:
                break
            
            curr_score = self.score(self.current_state)

            delta = n_score - self.current_score

            if delta > 0:
                self.current_state = s
                self.current_score = self.score(self.current_state)
            else:
                if random.uniform(0.0, 1.0) < exp(- delta / T):
                    self.current_state = s
                    self.current_score = self.score(self.current_state)
            

        return self.current_state

    def score(self, state) -> int:
        t = state.get_covered_targets_amount()
        budget = self.budget_left(state)    

        if budget < 0:
            return -1

        return 1000 * t + self.budget_left(state)

    def budget_left(self, state) -> int:
        N = state.get_placed_cables_amount()
        M = state.get_placed_routers_amount()

        return self.B - (N * self.Pb + M * self.Pr)
