class Graph:
    def __init__(self, vertices) -> None:
        self.V = len(vertices)
        self.vertices = list(vertices)
        self.graph = []

        for i in range(self.V - 1):
            for j in range(i + 1, self.V):
                u = self.vertices[i]
                v = self.vertices[j]

                w = self.weight(u, v)

                self.graph.append([i, j, w])

        # Amount of connections each vertex has on the MST
        # Used to place backbones on router with more than one connection
        self.childrenAmount = [0] * self.V


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

    def weight(self, u, v):
        """Calculates the Chebyshev distance between two points"""
        return max((abs(v[0] - u[0]), abs(v[1] - u[1]))) - 1

    def kruskal(self):
        self.graph = sorted(self.graph, key = lambda edge: edge[2])
        i, e = 0, 0
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
                self.childrenAmount[u] += 1
                self.childrenAmount[v] += 1
                self.apply_union(parent, rank, x, y)

    def get_mst_distance(self):
        result = 0
        
        for e in self.result:
            result += e[2]
            result += 1 if self.childrenAmount[e[0]] > 1 else 0
            result += 1 if self.childrenAmount[e[1]] > 1 else 0

            # Reset number of connections so that we dont put extra backbones
            self.childrenAmount[e[0]] = 0
            self.childrenAmount[e[1]] = 0

        return result - 1  # -1 because of the initial backbone
        # return sum([e[2] for e in self.result])