# graph.py
from typing import Dict, List, Any

class Node:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Node(id={self.id}, name='{self.name}')"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other): # type: ignore
        return isinstance(other, Node) and self.id == other.id

class Graph:
    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.adjacency_list: Dict[int, List[Dict[str, Any]]] = {}

    def add_node(self, node_id: int, node_name: str):
        if node_id not in self.nodes:
            new_node = Node(node_id, node_name)
            self.nodes[node_id] = new_node
            self.adjacency_list[node_id] = []

    def add_connection(self, node_a_id: int, node_b_id: int, distance: int):
        if node_a_id in self.nodes and node_b_id in self.nodes:
            self.adjacency_list[node_a_id].append({'node': self.nodes[node_b_id], 'distance': distance})
            self.adjacency_list[node_b_id].append({'node': self.nodes[node_a_id], 'distance': distance}) # Assuming undirected graph
        else:
            raise ValueError(f"One or both nodes ({node_a_id}, {node_b_id}) not found in graph.")

    def get_node_by_id(self, node_id: int) -> Node:
        return self.nodes.get(node_id) # type: ignore

    def get_node_by_name(self, node_name: str) -> Node | None:
        for node in self.nodes.values():
            if node.name.lower() == node_name.lower():
                return node
        return None

    def get_neighbors(self, node: Node) -> List[Dict[str, Any]]:
        return self.adjacency_list.get(node.id, [])