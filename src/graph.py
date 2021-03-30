class Graph:
    def __init__(self, vertices, parent_graph=None, removed_router=None, added_router=None) -> None:
        if parent_graph == None:
            self.vertices = list(vertices)
            self.edges = []

            for i in range(len(vertices) - 1):
                for j in range(i + 1, len(vertices)):
                    u = self.vertices[i]
                    v = self.vertices[j]
                    w = self.weight(u, v)

                    self.edges.append([i, j, w])

            # Amount of connections each vertex has on the minimum spanning tree
            # Used to place backbones on router with more than one connection
            self.children_amount = [0] * len(vertices)

        else:
            self.vertices = parent_graph.copy()
            self.edges = parent_graph.edges().copy()
            self.children_amount = parent_graph.children_amount.copy()

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

    @staticmethod
    def weight(u, v):
        """
        Calculates the Chebyshev distance between two points
        """

        return max((abs(v[0] - u[0]), abs(v[1] - u[1]))) - 1

    def kruskal(self):
        self.edges = sorted(self.edges, key=lambda edge: edge[2])
        i, e = 0, 0
        self.result = []
        parent = []
        rank = []

        for node in range(len(self.vertices)):
            parent.append(node)
            rank.append(0)

        while e < len(self.vertices) - 1:
            u, v, w = self.edges[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            if x != y:
                e += 1
                self.result.append([u, v, w])
                self.children_amount[u] += 1
                self.children_amount[v] += 1
                self.apply_union(parent, rank, x, y)

    def get_mst_distance(self):
        result = 0

        for e in self.result:
            result += e[2]
            result += 1 if self.children_amount[e[0]] > 1 else 0
            result += 1 if self.children_amount[e[1]] > 1 else 0

            # Reset number of connections so that we dont put extra backbones
            self.children_amount[e[0]] = 0
            self.children_amount[e[1]] = 0

        return result - 1  # -1 because of the initial backbone
