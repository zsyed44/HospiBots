from graph import Node
from graph import Graph

class Navigator:
    def __init__(self) -> None:
        pass 

    def determine_path(self, graph: Graph, from_node: Node, to_node: Node) -> list[Node]:
        raise NotImplementedError