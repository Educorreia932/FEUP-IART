import random

from math import exp

class Problem:
    # a)

    def __init__(self) -> None:
        """Initial random solution"""
        self.Ns = 4     # Number of slots
        self.Nd = 12    # Number of disciplines
        self.Na = 12    # Number of students
        self.enrolled = [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9],
            [10, 11, 12],
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [1, 2, 3, 5],
            [6, 7, 8],
            [4, 9, 10, 11, 12],
            [1, 2, 4, 5],
            [3, 6, 7, 8],
            [9, 10, 11, 12]
        ]
        self.solution = [random.randrange(self.Ns) for _ in range(self.Nd)]    # Allocate disciplines into slots

    # b)

    def incompatibilities(self, d1: int, d2: int) -> int:
        return len(set(self.enrolled[d1]).intersection(set(self.enrolled[d2])))

    # c)

    def evaluate(self, solution) -> int:
        evaluation = 0

        for d1 in range(self.Nd - 1):
            for d2 in range(d1 + 1, self.Nd):
                if solution[d1] == solution[d2]:
                    evaluation += self.incompatibilities(d1, d2)

        return evaluation

    # d)

    def neighbour1(self, solution):
        """Change a discipline from slot"""
        d1 = random.randrange(self.Nd)
        new_slot = random.randrange(self.Ns)

        while new_slot == solution[d1]:
            new_slot = random.randrange(self.Ns)

        solution[d1] = new_slot

        return solution

    def neighbour2(self, solution):
        """Exchange the slots of two disciplines"""
        d1 = random.randrange(self.Nd)
        d2 = random.randrange(self.Nd)

        while d1 == d2 or solution[d1] == solution[d2]:
            d2 = random.randrange(self.Nd)

        solution[d1], solution[d2] = solution[d2], solution[d1] 

        return solution

    def neighbour3(self, solution):
        """Change a discipline from slot or exchange the slots of two disciplines"""

        if random.choice([True, False]):
            return self.neighbour1(solution)

        else:
            return self.neighbour2(solution)

    # e)

    def hill_climbing(self):
        solution = self.solution.copy()
        i = 0
        
        while i < 1000:
            neighbour = self.neighbour3(solution.copy())
            i += 1

            if self.evaluate(neighbour) < self.evaluate(solution):
                solution = neighbour
                i = 0

        return solution

    def simulated_annealing(self):
        solution = self.solution.copy()
        i = 0
        T = 1000 

        while i < 1000:
            T *= 0.9
            neighbour = self.neighbour3(solution.copy())
            delta = self.evaluate(solution) - self.evaluate(neighbour)
            i += 1

            if delta > 0 or exp(-delta / T) > random.random():
                solution = neighbour
                i = 0

        return solution

if __name__ == "__main__":
    problem = Problem()

    s1 = problem.hill_climbing()
    s2 = problem.simulated_annealing()

    print(s1)
    print(s2)
