from copy import deepcopy

from src.cell import Cell
from src.grid import Grid
from src.state import State


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
        for i in range(self.grid.H):
            for j in range(self.grid.W):
                cell = self.grid.get_cell((i, j))

                if cell != Cell.WALL and cell != Cell.ROUTER:
                    new_state = deepcopy(self.current_state)
                    new_state.place_router((i, j), self.R)

                    yield new_state

    def normal_hillclimb(self) -> State:
        neighbour_states = self.generate_new_states()

        while True:
            neighbour = next(neighbour_states)
            neighbour_score = self.score(neighbour)

            if neighbour_score <= self.current_score:
                return self.current_state

            self.current_state = neighbour
            self.current_score = neighbour_score
            neighbour_states = self.generate_new_states()

    def hillclimb_steepest_ascent(self) -> State:
        counter = 0

        while True:
            print(counter)
            counter += 1

            neighbour = max(self.generate_new_states(), key=self.score)
            neighbour_score = self.score(neighbour)

            if neighbour_score <= self.current_score:
                return self.current_state

            self.current_state = neighbour
            self.current_score = neighbour_score

    def score(self, state) -> int:
        l = state.get_covered_targets_amount()
        N = state.get_placed_backbones_amount()
        M = state.get_placed_routers_amount()

        return 1000 * l + (self.B - N * self.Pb + M * self.Pr)
