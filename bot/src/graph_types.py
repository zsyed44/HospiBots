from typing import TypedDict, List

# The structure of a single node as it appears in JSON
class JsonNodeData(TypedDict):
    id: int
    name: str

# The structure of a single connection as it appears in JSON
class JsonConnectionData(TypedDict):
    node_a: int
    node_b: int
    distance: float

# The overall structure of the JSON data
class JsonGraphData(TypedDict):
    nodes: List[JsonNodeData]
    connections: List[JsonConnectionData]