class Graph:
    def __init__(self) -> None:
        self.graph = {}

    def add_edge(self, src, dst): 
        if src not in self.graph: 
            self.graph[src] = [dst]
        else: 
            self.graph[src].append(dst)

    def bfs(self, start):
        visited = set()
        q = [start]
        while q:
            v = q.pop()
            if v not in visited:
                print(f"{v} ->", end=" ")
                visited.add(v)
                neigh = self.graph.get(v, [])
                q.extend(neigh)
        print()

    def print_graph(self):
        for vertex, neighbors in self.graph.items():
            print(f"Vertex {vertex}: {', '.join(neighbors)}")

graph = Graph()

graph.add_edge("A", "B")
graph.add_edge("A", "C")
graph.add_edge("B", "C")
graph.add_edge("B", "D")
graph.add_edge("C", "D")

# print(graph.graph)
graph.bfs("A")

graph.print_graph()





