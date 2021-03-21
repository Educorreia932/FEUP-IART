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

                    self.graph.append([i, j, w])

            self.graph = sorted(self.graph, key=lambda item: item[2])

        else:
            self.vertices = parent_graph.vertices.copy()
            self.graph = parent_graph.graph.copy()

            # Case for more than one new vertex
            for i in range(len(new_vertices)):
                for j in range(len(self.vertices)):
                    u = new_vertices[i]
                    v = self.vertices[j]

                    w = self.weight(u, v)

                    self.add_edge(parent_graph.V + i, j, w)

            self.vertices.extend(new_vertices)
            self.V = len(self.vertices)

        self.childrenAmount = [0]*self.V

    def add_edge(self, u, v, w):

        i = binary_search(self.graph, w, 0, len(self.graph) - 1)
        self.graph.insert(i, [u, v, w])

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
            self.childrenAmount[e[0]] = 0
            self.childrenAmount[e[1]] = 0

        return result - 1 # -1 because of the initial backbone
        # return sum([e[2] for e in self.result])


def binary_search(arr, val, start, end):
    # We need to distinguish whether we should insert before or after the left boundary. 
    # Imagine [0] is the last step of the binary search and we need to decide where to insert -1
    if start == end:
        if arr[start][2] > val:
            return start
            
        else:
            return start+1

    # This occurs if we are moving beyond left's boundary
    # Meaning the left boundary is the least  position to find a number greater than val
    if start > end:
        return start

    mid = (start + end) // 2

    if arr[mid][2] < val:
        return binary_search(arr, val, mid+1, end)

    elif arr[mid][2] > val:
        return binary_search(arr, val, start, mid-1)

    else:
        return mid