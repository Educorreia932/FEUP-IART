from rich import print

def read_file(filename):
    with open(filename) as file:
        lines = file.read().split("\n")

        rows, columns, router_range_radius = [int(x) for x in lines[0].split()]
        backbone_cost, router_cost, budget = [int(x) for x in lines[1].split()]
        x, y = [int(x) for x in lines[2].split()]

        grid = []

        for i in range(3, rows):
            row = []

            for j in range(columns):
                row.append(lines[i][j])

            grid.append(row)

        print(rows, columns, router_range_radius)
        print(backbone_cost, router_cost, budget)
        print(x, y)
        print(grid)

if __name__ == "__main__":
    read_file("input/example.in")
