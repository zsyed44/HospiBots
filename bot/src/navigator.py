# navigator.py
import heapq
from collections import deque
from graph import Graph, Node
from typing import List, Tuple, Dict, Optional # Added Any for the tie-breaker

class Navigator:
    def __init__(self):
        pass

    def find_shortest_path(self, graph: Graph, start_node: Node, end_node: Node) -> Optional[List[Node]]:
        """
        Implements Dijkstra's algorithm to find the shortest path between two nodes.

        Args:
            graph: The Graph object containing nodes and connections.
            start_node: The starting Node.
            end_node: The destination Node.

        Returns:
            A list of Nodes representing the shortest path, or None if no path exists.
        """
        # Dictionary to store the shortest distance from start_node to every other node
        distances: Dict[Node, float] = {node: float('inf') for node in graph.nodes.values()}
        distances[start_node] = 0

        # Dictionary to reconstruct the path
        previous_nodes: Dict[Node, Optional[Node]] = {node: None for node in graph.nodes.values()}

        # Priority queue to store (distance, tie_breaker, node) tuples.
        # The tie_breaker is crucial for handling cases where distances are equal
        # and preventing TypeError on Node comparison.
        priority_queue: List[Tuple[float, int, Node]] = []
        heapq.heappush(priority_queue, (0, 0, start_node)) # (distance, tie_breaker, node)
        
        # A simple counter for tie-breaking
        tie_breaker_counter = 0

        while priority_queue:
            current_distance, _, current_node = heapq.heappop(priority_queue) # Ignore tie_breaker

            # If we've already found a shorter path to current_node, skip
            if current_distance > distances[current_node]:
                continue

            # If we reached the end node, reconstruct the path
            if current_node == end_node:
                path: deque[Node] = deque()
                current = end_node
                while current:
                    path.appendleft(current)
                    current = previous_nodes[current]
                return list(path)

            # Explore neighbors
            for neighbor_info in graph.get_neighbors(current_node):
                neighbor_node = neighbor_info['node']
                weight = neighbor_info['distance']
                distance = current_distance + weight

                # If a shorter path to the neighbor is found
                if distance < distances[neighbor_node]:
                    distances[neighbor_node] = distance
                    previous_nodes[neighbor_node] = current_node
                    tie_breaker_counter += 1 # Increment for unique tie-breaker
                    heapq.heappush(priority_queue, (distance, tie_breaker_counter, neighbor_node))

        return None # No path found