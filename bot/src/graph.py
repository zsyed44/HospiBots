""" 
This is the graph that forms a floor plan that bots navigate.

Graphs are non-directed, weighted, and topologically flat (node's sibling order is important).
The assumption is that node sibling order is counter-clockwise.
"""

import json
import os
from collections import deque

from graph_types import *

ALLOW_SELF_LOOPS = False

class Node:
    def __init__(self, id: int, name: str, siblings: dict["Node", float]) -> None:
        self.id = id
        self.name = name 
        self.siblings = siblings

    @property
    def neighbors(self):
        return self.siblings

class Connection:
    def __init__(self, node_a_id: int, node_b_id: int, distance: float):
        self.node_a_id = node_a_id
        self.node_b_id = node_b_id
        self.distance = distance

    def involves_node(self, node: Node) -> bool:
        return self.involves_id(node.id)
    
    def involves_id(self, id: int):
        return self.node_a_id == id or self.node_b_id == id
    
    def get_other_id(self, id: int) -> int:
        """
        Returns the id of the node that doesn't have this given id.
        If the given id isn't in this connection, throw an error.

        Args:
            id (int): The id of the node that shouldn't be returned in the connection.

        Returns:
            int: The other node's id
        """
        if id == self.node_a_id:
            return self.node_b_id
        elif id == self.node_b_id:
            return self.node_a_id

        else:
            raise Exception(f'Node with id {id} doesn\'t exist in this connection!')

    def __eq__(self, other: object):
        if isinstance(other, "Connection"):
            return {self.node_a_id, self.node_b_id} == {other.node_a_id, other.node_b_id}
        
        else:
            return False
        
    def __hash__(self) -> int:
        # Generate a hash based on the immutable attributes that determine equality.
        return hash((self.node_a_id, self.node_b_id))

class Graph:
    def __init__(self) -> None:
        self._nodes: set[int] = set()
        self._node_names: dict[int, str] = dict()
        self._connections: set[Connection] = set()

    def get_one_node_id(self) -> int:
        """
        Returns a node id from this graph. No guarantee of where this comes from or anything about it but it is in the graph.

        Raises:
            Exception: _description_

        Returns:
            int: id of a node in the graph
        """
        if not self._nodes or len(self._nodes) < 1:
            raise Exception('Graph is empty, cannot get one node!')
        
        return next(iter(self._nodes))
    
    def get_one_node(self) -> Node:
        return self.get_node(self.get_one_node_id())

    @property
    def node_ids(self) -> set[int]:
        """
        Provides read only access to node IDs

        Returns:
            set[int]: The set of node ids in the graph
        """
        return self._nodes

    def create_node(self, id: int, name: str):
        if id in self._nodes:
            raise Exception(f'Node {id} already exists in this graph!')
        
        self._nodes.add(id)
        self._node_names[id] = name
    
    def get_node(self, id: int) -> Node:
        name = self._node_names[id]
        siblings_ids: dict[int, float] = {c.get_other_id(id): c.distance for c in self._connections if c.involves_id(id)}
        siblings = {self.get_node(id) : distance for (id, distance) in siblings_ids.items()}

        return Node(id, name, siblings)

    def create_connection(self, conn: Connection):
        self._connections.add(conn)

    def is_fully_connected(self) -> bool:
        """
        Checks if a graph is fully connected, meaning all nodes are reachable
        from each other.

        Args:
            graph: A dictionary representing the graph.
                Keys are nodes, and values are lists of their siblings (neighbors).
                Example: {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']}

        Returns:
            True if the graph is fully connected, False otherwise.
        """
        # An empty graph or a graph with a single node is considered fully connected.
        if not self._nodes or len(self._nodes) == 1:
            return True

        # Start BFS from the first node in the graph
        start_node_index = 0

        # Set to keep track of visited nodes during BFS
        visited: set[int] = set()

        # Queue for BFS traversal
        queue: deque[int] = deque()

        # Add the starting node to the queue and mark it as visited
        queue.append(start_node_index)
        visited.add(start_node_index)

        # Perform BFS traversal
        while queue:
            current_node_id = queue.popleft()

            # Iterate over the siblings (neighbors) of the current node
            for neighbor_id in [c.get_other_id(current_node_id) for c in self._connections if c.involves_id(current_node_id)]: # Use .get() to handle nodes not explicitly having siblings defined
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append(neighbor_id)

        # If the number of visited nodes equals the total number of nodes,
        # the graph is fully connected.
        return len(visited) == len(self._nodes)

def load_graph_from_json_file(json_path: str) -> Graph:
    absolute_path_attempt = os.path.abspath(json_path)
    print(f"Attempted absolute path: {absolute_path_attempt}")
    # open json file
    with open(json_path, 'r') as file:
        data = json.load(file)

        return load_graph_from_json(data)
    
    raise Exception(f"Unknown error, failed to parse graph from {json_path}")


def load_graph_from_json(data: JsonGraphData) -> Graph: # type: ignore
    graph = Graph()

    # create all the nodes first
    for nodeData in data['nodes']:
        id = int(nodeData['id'])
        name = str(nodeData['name'])
        graph.create_node(id, name)

    # then populate their siblings
    for index, connection in enumerate(data['connections']):
        node_a_id: int = connection['node_a']
        node_b_id: int = connection['node_b']
        distance: float = connection['distance']

        # Check if self-loops are allowed
        if not ALLOW_SELF_LOOPS and node_a_id == node_b_id:
            raise Exception(f'Failed to parse graph data, self-loop in connection {index} between {node_a_id} and {node_b_id} is not allowed.')

        # Check if these nodes exist
        if not {node_a_id, node_b_id}.intersection(graph.node_ids):
            raise Exception(f'Failed to parse graph data! Can\'t create connection {index} as node {node_a_id} or {node_b_id} does not exist!')
        
        # If passed, update node's siblings
        graph.create_connection(Connection(node_a_id, node_b_id, distance)) # type: ignore
        
    # make some assertions
    assert len(graph.node_ids) == len(data['nodes']), f"Failed to parse graph data."
    assert graph.is_fully_connected(), f"Assertion error, graph is not fully connected!"
    
    # return the graph
    return graph