import heapq

from graph import Graph

def dijkstra(graph: Graph, start_node_id: int):
    """
    Finds the shortest paths from a start_node to all other nodes in an undirected,
    weighted graph using Dijkstra's algorithm.

    Args:
        graph (dict): An adjacency list representation of the graph.
                      Keys are nodes, values are dictionaries of neighbors
                      and their edge weights.
                      Example: {'A': {'B': 1, 'C': 4}, 'B': {'A': 1, 'C': 2, 'D': 5}}
        start_node: The node from which to start finding shortest paths.

    Returns:
        dict: A dictionary where keys are nodes and values are their shortest
              distances from the start_node. Returns float('inf') for unreachable nodes.
    """
    
    # Initialize distances: all to infinity, start_node to 0
    distances: dict[int, float] = {node_id: float('infinity') for node_id in graph.node_ids}
    distances[start_node_id] = 0

    # Priority queue to store (distance, node_id) pairs.
    # The smallest distance node is always at the top.
    priority_queue = [(0.0, start_node_id)]  # (distance, node)

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we've already found a shorter path to this node, skip it
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        neighbors = graph.get_node(current_node).neighbors
        for (neighbor, weight) in neighbors.items():
            distance = current_distance + weight

            # If a shorter path to the neighbor is found
            if distance < distances[neighbor.id]:
                distances[neighbor.id] = distance
                heapq.heappush(priority_queue, (distance, neighbor.id))

    return distances