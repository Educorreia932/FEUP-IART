import numpy as np

from enum import IntEnum

class Cell(IntEnum):
    BACKBONE = -2
    VOID = -1
    WALL = 0
    WIRELESS = 1
    ROUTER = 2
    CONNECTED_ROUTER = 3
    CABLE = 4

    @classmethod
    def from_character(cls, character):
        cell_characters = {
            "-": Cell.VOID,
            "#": Cell.WALL,
            ".": Cell.WIRELESS
        }

        if character in cell_characters:
            return cell_characters[character]

        raise ValueError(f"{character} is not a valid cell character.")

def read_file(filename):
    with open(filename) as file:
        lines = file.read().split("\n")

        H, W, R = [int(x) for x in lines[0].split()]
        Pb, Pr, B = [int(x) for x in lines[1].split()]
        br, bc = [int(x) for x in lines[2].split()]

        grid = np.zeros((H, W), dtype=np.int8)

        for i in range(3, H):
            for j in range(W):
                grid[i, j] = Cell.from_character(lines[i][j])


if __name__ == "__main__":
    read_file("input/example.in")
