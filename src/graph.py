class Graph:
    def __init__(self, new_vertices, parent_graph=None):
        if parent_graph == None:
            self.V = len(new_vertices)
            self.vertices = list(new_vertices)
            self.graph = []

            for i in range(self.V - 1):
                for j in range(i + 1, self.V):
                    u = self.vertices[i]
                    v = self.vertices[j]

                    w = self.weight(u, v)

                    self.add_edge(i, j, w)

        else:
            self.vertices = parent_graph.vertices.copy()
            self.graph = parent_graph.graph.copy()

            # Case for more than one new vertex
            for i in range(len(self.vertices), len(self.vertices) + len(new_vertices)):
                for j in range(len(self.vertices)):
                    u = new_vertices[i - len(self.vertices)]
                    v = self.vertices[j]

                    w = self.weight(u, v)

                    self.add_edge(i, j, w)

            self.vertices.extend(new_vertices)
            self.V = len(self.vertices)


    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    # Search function

    def find(self, parent, i):
        if parent[i] == i:
            return i

        return self.find(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot

        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot

        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def weight(_, u, v):
        """Taken from https://en.wikipedia.org/wiki/Chebyshev_distance"""
        return max((abs(v[0] - u[0]), abs(v[1] - u[1]))) - 1

    #  Applying Kruskal algorithm

    def kruskal(self):
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        self.result = []
        parent = []
        rank = []

        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        while e < self.V - 1:
            u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            if x != y:
                e += 1
                self.result.append([u, v, w])
                self.apply_union(parent, rank, x, y)

    def get_mst_distance(self):
        return sum([e[2] for e in self.result])
