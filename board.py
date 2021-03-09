from cell import Cell


class Board():

    def __init__(self, h, w, grid):
        self.h = h
        self.w = w
        self.grid = grid

    def get_cell(self, coords):
        return self.grid[coords[0]][coords[1]]

    def generate_neighbours(self, coords):
        # result = []
        # for i in [-1, 0, 1]:
        #     for j in [-1, 0, 1]:
        #         if 0 <= i + coords[0] < self.h and 0 <= j + coords[1] < self.w and ((i + coords[0]) != (j + coords[1])):
        #             if self.grid[i + coords[0]][j + coords[1]] != Cell.WALL:
        #                 result.append([coords[0] + i, coords[1] + j])
        # return result
        return [(coords[0] + i, coords[1] + j) for i in [-1, 0, 1] for j in [-1, 0, 1] if 0 <= i + coords[0] < self.h and 0 <= j + coords[1] < self.w and i + coords[0] != j + coords[1] and self.grid[i + coords[0]][j + coords[1]] != Cell.WALL]

    # ineficiente
    def router_can_see(self, r_coords, target):
        top = min(target[0], r_coords[0])
        bottom = max(target[0], r_coords[0])

        left = min(target[1], r_coords[1])
        right = max(target[1], r_coords[1])

        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                if self.grid[i][j] == Cell.WALL:
                    return False

        return True

    def __str__(self):
        result = ""
        for line in self.grid:
            for elem in line:
                result += Cell.to_character(elem) + " "
            result += "\n"

        return result
