class Node:
    def __init__(self, id: int, name: str, siblings: dict["Node", float]={}) -> None:
        self.id = id
        self.name = name 
        self.siblings = siblings

    def add_neighbor(self, node: "Node", distance: float):
        self.siblings[node] = distance

    @property
    def neighbors(self):
        return self.siblings
