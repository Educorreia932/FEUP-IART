import time

from io import *

from solution import read_file

if __name__ == "__main__":
    problem = read_file("../input/charleston_road.in")
    
    start = time.time()

    end = time.time()

    print(f"Elapsed time of execution is {end - start} seconds.")
    