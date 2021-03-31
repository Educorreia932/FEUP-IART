class Graph:
    def __init__(self, vertices=None, parent_graph=None) -> None:
        if parent_graph == None:
            self.vertices = list(vertices)
            self.V = len(vertices)
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
            self.vertices = parent_graph.vertices.copy()
            self.V = parent_graph.V
            self.edges = parent_graph.edges.copy()
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

    def kruskal(self):
        self.edges = sorted(self.edges, key=lambda edge: edge[2])
        i, e = 0, 0
        self.result = []
        parent = []
        rank = []

        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        while e < self.V - 1:
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

    def get_mst_distance(self) -> int:
        """
        Get the MST total weight, that is, the sum of each edge's weight.
        """

        total_weight = 0

        for e in self.result:
            total_weight += e[2]
            total_weight += 1 if self.children_amount[e[0]] > 1 else 0
            total_weight += 1 if self.children_amount[e[1]] > 1 else 0

            # Reset number of connections so that we dont put extra backbones
            self.children_amount[e[0]] = 0
            self.children_amount[e[1]] = 0

        return total_weight - 1  # -1 because of the initial backbone

    def moved_router(self, before, after):
        self.removed_router(before)
        self.added_router(after)

    def added_router(self, router):
        self.vertices.append(router)

        for i in range(self.V):
            v = self.vertices[i]
            w = self.weight(router, v)
            self.edges.append([self.V, i, w])

        self.V += 1
        self.children_amount = [0] * self.V

    def removed_router(self, router):
        """
        Update graph information after removing a router.
        """

        router_index = self.vertices.index(router)
        self.vertices.pop(router_index)

        E = len(self.edges)  # Total number of edges
        i = 0

        while i < E:
            if router_index in (self.edges[i][0], self.edges[i][1]):
                self.edges.pop(i)
                E -= 1

            else:
                i += 1

        for i in range(len(self.edges)):
            if self.edges[i][0] > router_index:
                self.edges[i][0] -= 1

            if self.edges[i][1] > router_index:
                self.edges[i][1] -= 1

        self.V -= 1
        self.children_amount = [0] * self.V

    @staticmethod
    def weight(u, v):
        """
        Calculates the Chebyshev distance between two points
        """

        return max((abs(v[0] - u[0]), abs(v[1] - u[1]))) - 1
