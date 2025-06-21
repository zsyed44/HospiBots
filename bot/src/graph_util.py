import json 
import os 

from graph import Graph

def build_graph_from_json(json_data: str) -> Graph:
    """
    Builds a Graph object from a JSON string.

    Args:
        json_data: A string containing the JSON representation of nodes and connections.

    Returns:
        A populated Graph object.
    """
    data = json.loads(json_data)
    my_graph = Graph()

    for node_data in data['nodes']:
        my_graph.add_node(node_data['id'], node_data['name'])

    for conn_data in data['connections']:
        my_graph.add_connection(conn_data['node_a'], conn_data['node_b'], conn_data['distance'])
    
    return my_graph

def build_graph_from_json_file(json_path: str) -> Graph:
    """
    Builds a Graph object by reading JSON data from a file.

    Args:
        json_path: The file path to the JSON document.

    Returns:
        A populated Graph object.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found at path: {json_path}")

    try:
        with open(json_path, 'r') as f:
            json_data = f.read()
        return build_graph_from_json(json_data)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON from file {json_path}: {e.msg}", e.doc, e.pos)
