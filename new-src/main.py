import time

from in_out import *

if __name__ == "__main__":
    problem = read_file("input/charleston_road.in")
    
    start = time.time()

    problem.hill_climbing()

    end = time.time()

    print(f"Elapsed time of execution is {end - start} seconds.")
    