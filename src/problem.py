import random

from copy import deepcopy

from cell import Cell
from grid import Grid
from state import State


class Problem:
    def __init__(self, H, W, R, Pb, Pr, budget, backbone, cells):
        self.R = R
        self.Pb = Pb
        self.Pr = Pr
        self.B = budget

        self.grid = Grid(H, W, cells)
        self.current_state = State(backbone, self.grid)
        self.current_score = self.score(self.current_state)

    def __str__(self):
        return self.grid.__str__()

    def generate_new_states(self):
        n = self.current_state.get_uncovered_targets_amount()

        for _ in range(n):
            coords = random.choice(tuple(self.current_state.uncovered_targets))

            new_state = deepcopy(self.current_state)
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

            if len(neighbour_states) == 0:
                return self.current_state

            neighbour = max(neighbour_states, key=self.score)
            neighbour_score = self.score(neighbour)

            if neighbour_score <= self.current_score:
                return self.current_state

            self.current_state = neighbour
            self.current_score = neighbour_score

    def score(self, state) -> int:
        t = state.get_covered_targets_amount()
        N = state.get_placed_cables_amount()
        M = state.get_placed_routers_amount()

        budget = self.B - (N * self.Pb + M * self.Pr)

        if budget < 0:
            return -1

        return 1000 * t + budget
