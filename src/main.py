import time

from in_out import *

if __name__ == "__main__":
    selected_building, selected_algorithm = user_input()

    problem: Problem = read_file(selected_building)

    start: float = time.time()

    solution: Solution = selected_algorithm(problem)

    end: float = time.time()

    print()
    print(f"Elapsed time of execution is {end - start} seconds.")
    print(f"Final score: {solution.evaluate()}")
    print(f"Covered cells: {solution.covered_cells}")
    print(f"Placed routers: {len(solution.get_placed_routers())}")

    plot(solution)
    
