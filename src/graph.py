class Vertex():
    def __init__(self, coords):
        self.coords = coords
        self.dist = None
        self.path = None

    def get_coords(self):
        return self.coords

    def __repr__(self) -> str:
        return "Vertex: " + self.coords.__repr__()


class Graph():
    def __init__(self, vertices):
        self.vertices = [Vertex(coords) for coords in vertices]
        self.edges = []

        for v1 in self.vertices:
            for v2 in self.vertices:
                self.add_edge(v1, v2, self.weight(v1, v2))

    def add_edge(self, u, v, w):
        """Add an edge to graph"""
        self.edges.append([u, v, w])

    def find(self, u):
        """Find set of an element i (uses path compression technique)"""
        while u != u.path:
            u = u.path
        return u

    def union(self, u, v):
        a = self.find(u)
        b = self.find(v)

        if a.get_coords() == b.get_coords():
            return

        if a.dist > b.dist:
            b.path = a

        else:
            a.path = b

            if a.dist == b.dist:
                b.dist += 1

    # based on the implementation of the UC CAL
    def kruskal(self):
        for v in self.vertices:
            v.dist = 0
            v.path = v

        self.edges.sort(key=lambda e: e[2])

        for e in self.edges:
            u = e[0]
            v = e[1]

            if self.find(u).get_coords() != self.find(v).get_coords():
                self.union(u, v)

    def weight(self, u, v):
        """Taken from https://en.wikipedia.org/wiki/Chebyshev_distance"""
        return max((abs(v.coords[0] - u.coords[0]), abs(v.coords[1] - u.coords[1]))) - 1

    def __str__(self) -> str:

        result = ""

        for _ in self.vertices:
            result += result.__str__() + "\n"

        return result

    def get_mst_distance(self):
        return sum([self.weight(v, v.path) for v in self.vertices if v != v.path])
