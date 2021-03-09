from enum import IntEnum


class Cell(IntEnum):
    BACKBONE = -2
    VOID = -1
    WALL = 0
    TARGET = 1
    ROUTER = 2
    CONNECTED_ROUTER = 3  # Places where the router reaches
    CABLE = 4

    @classmethod
    def from_character(cls, character):
        cell_characters = {
            "-": Cell.VOID,
            "#": Cell.WALL,
            ".": Cell.TARGET
        }

        if character in cell_characters.keys():
            return cell_characters[character]

        raise ValueError(f"{character} is not a valid cell character.")

    @classmethod
    def to_character(cls, cell):
        cell_characters = {
            Cell.VOID: "-",
            Cell.WALL: "#",
            Cell.TARGET: ".",
            Cell.ROUTER: "r",
            Cell.BACKBONE: "b",
            Cell.CONNECTED_ROUTER: "c"
        }

        return cell_characters[cell]
