import time

from in_out import *

if __name__ == "__main__":
    # problem = read_file("input/example.in")
    # problem = read_file("input/charleston_road.in")
    problem = read_file("input/rue_de_londres.in")
    # problem = read_file("input/opera.in")
    
    start = time.time()

    # solution = problem.hill_climbing()
    # solution = problem.hill_climbing_steepest_ascent()
    solution = problem.simmulatead_annealing()

    end = time.time()

    print(f"Elapsed time of execution is {end - start} seconds.")
    print(f"Final score: {solution.evaluate()}")

    plot(solution)
    