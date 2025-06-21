from graph import Graph
from node import Node

from typing import Optional, List, Dict, Set, Tuple
import heapq

class Navigator:
    def __init__(self) -> None:
        pass 

    def determine_path(self, graph: Graph, from_node: Node, to_node: Node) -> List[Node]:
        """
        Determines the shortest path between two nodes in a graph using Dijkstra's algorithm.

        Args:
            graph (Graph): The graph representing the floor plan.
            from_node (Node): The starting node.
            to_node (Node): The destination node.

        Returns:
            List[Node]: A list of Node objects representing the shortest path
                        from from_node to to_node.
                        Returns an empty list if no path exists or if start/end nodes
                        are not found in the graph.
        Raises:
            ValueError: If the start or destination node is not found in the graph.
        """
        # Validate that start and end nodes actually exist in the graph's registered nodes
        if from_node.id not in graph.node_ids:
            raise ValueError(f"Starting node with ID {from_node.id} not found in graph.")
        if to_node.id not in graph.node_ids:
            raise ValueError(f"Destination node with ID {to_node.id} not found in graph.")

        start_node_id = from_node.id
        end_node_id = to_node.id

        # distances: Stores the shortest distance found so far from start_node_id to each node ID.
        # Initialized with infinity for all nodes except the start_node_id.
        distances: Dict[int, float] = {node.id: float('inf') for node in graph.nodes} # Iterate over graph._nodes for all node IDs
        distances[start_node_id] = 0.0

        # previous_nodes: Stores the predecessor of each node ID in the shortest path found so far.
        # Used to reconstruct the path after the algorithm completes.
        previous_nodes: Dict[int, Optional[int]] = {node.id: None for node in graph.nodes} # Iterate over graph._nodes for all node IDs

        # priority_queue: A min-heap to store (distance, node_id) tuples.
        # heapq ensures that the node with the smallest current distance is always
        # extracted next, which is fundamental to Dijkstra's.
        priority_queue: List[Tuple[float, int]] = [(0.0, start_node_id)]

        # visited_node_ids: A set to keep track of nodes whose shortest path
        # from the start has been finalized. Once a node is visited, its
        # shortest path is known.
        visited_node_ids: Set[int] = set()

        while priority_queue:
            # Extract the node with the smallest distance from the priority queue.
            current_distance, current_node_id = heapq.heappop(priority_queue)

            # If this node has already been visited (i.e., its shortest path has
            # already been finalized), we can skip it. This handles cases where
            # a node might be added to the queue multiple times with different distances.
            if current_node_id in visited_node_ids:
                continue

            # Mark the current node as visited, as its shortest path is now known.
            visited_node_ids.add(current_node_id)

            # If we've reached the destination node, we have found the shortest path
            # to it, and we can terminate the main loop.
            if current_node_id == end_node_id:
                break

            # Get the actual Node object to access its neighbors
            current_node_obj = graph.get_node(current_node_id)

            # Iterate over neighbors of the current node
            # The neighbors property returns a dict[Node, float]
            for neighbor_node, weight in current_node_obj.neighbors.items():
                neighbor_id = neighbor_node.id

                # Only consider unvisited neighbors for relaxation
                if neighbor_id not in visited_node_ids:
                    # Calculate the new potential distance to the neighbor through the current node
                    distance_through_current = current_distance + weight

                    # If this newly calculated path to the neighbor is shorter
                    # than any path found so far, update it.
                    if distance_through_current < distances[neighbor_id]:
                        distances[neighbor_id] = distance_through_current
                        previous_nodes[neighbor_id] = current_node_id
                        # Add (or re-add with updated distance) the neighbor to the priority queue
                        heapq.heappush(priority_queue, (distance_through_current, neighbor_id))

        # Reconstruct the path from destination to source using the previous_nodes dictionary.
        path: List[Node] = []
        current_path_node_id = end_node_id

        # If the distance to the end node is still infinity, it means no path was found.
        if distances[end_node_id] == float('inf'):
            return []

        # Backtrack from the end node until the start node (or None if path broken)
        while current_path_node_id is not None:
            # Convert the node ID back to a Node object using the graph's get_node method
            path.append(graph.get_node(current_path_node_id))
            # Move to the previous node in the shortest path
            current_path_node_id = previous_nodes[current_path_node_id]

        # The path was built in reverse order (from end to start), so reverse it
        # to get the path from start to end.
        return path[::-1]

