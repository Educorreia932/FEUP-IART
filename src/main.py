import time

from in_out import *

if __name__ == "__main__":
    selected_building, selected_algorithm = user_input()

    problem = read_file(selected_building)

    start = time.time()

    solution = selected_algorithm(problem)

    end = time.time()

    print(f"Elapsed time of execution is {end - start} seconds.")
    print(f"Final score: {solution.evaluate()}")

    plot(solution)
    