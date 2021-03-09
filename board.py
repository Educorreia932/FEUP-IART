from cell import Cell

class Board():

    def __init__(self, h, w, grid):
        self.h = h
        self.w = w
        self.grid = grid

    def generate_neighbours(self, coords):
        # result = []
        # for i in [-1, 0, 1]:
        #     for j in [-1, 0, 1]:
        #         if 0 <= i + coords[0] < self.h and 0 <= j + coords[1] < self.w and ((i + coords[0]) != (j + coords[1])):
        #             if self.grid[i + coords[0]][j + coords[1]] != Cell.WALL:
        #                 result.append([coords[0] + i, coords[1] + j])
        # return result
        return [[coords[0] + i, coords[1] + j] for i in [-1, 0, 1] for j in [-1, 0, 1] if 0 <= i + coords[0] < self.h and 0 <= j + coords[1] < self.w and i + coords[0] != j + coords[1] and self.grid[i + coords[0]][j + coords[1]] != Cell.WALL]


if __name__ == "__main__":
    b = Board(10, 10, [[1]*10]*10)

    print(b.generate_neighbours([5,5]))