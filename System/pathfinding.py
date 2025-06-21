from dijkstar import Graph, find_path

graph = Graph()

graph.add_edge('A', 'B', 1)
graph.add_edge('B', 'A', 1)
graph.add_edge('A', 'C', 2)
graph.add_edge('C', 'A', 2)
graph.add_edge('B', 'C', 3)
graph.add_edge('C', 'B', 3)
graph.add_edge('B', 'D', 1)
graph.add_edge('D', 'B', 1)
graph.add_edge('B', 'E', 1)
graph.add_edge('E', 'B', 1)
graph.add_edge('C', 'F', 1)
graph.add_edge('F', 'C', 1)
graph.add_edge('D', 'F', 2)
graph.add_edge('F', 'D', 2)
graph.add_edge('D', 'H', 2)
graph.add_edge('H', 'D', 2)
graph.add_edge('F', 'G', 1)
graph.add_edge('G', 'F', 1)
graph.add_edge('G', 'H', 1)
graph.add_edge('H', 'G', 1)

print(find_path(graph, 'F', 'B'))

# In simple terms, this graph stores every node (shown in the hospital_layout.png file), 
# based on each node and its direct neighbors
hospital_graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D', 'E'],
    'C': ['A', 'B', 'F'],
    'D': ['B', 'F', 'H'],
    'E': ['B'],
    'F': ['C', 'D', 'G'],
    'G': ['F', 'H'],
    'H': ['D', 'G']
}

