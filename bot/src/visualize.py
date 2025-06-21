
def visualize_graph(graph: Graph):
    import json
    import networkx as nx
    import matplotlib.pyplot as plt

    # Create a graph
    G = nx.Graph()

    # Add nodes and store names
    node_labels = {}
    for node in graph_data["nodes"]:
        G.add_node(node["id"], name=node["name"])
        node_labels[node["id"]] = node["name"]

    # Add edges
    for connection in graph_data["connections"]:
        G.add_edge(connection["node_a"], connection["node_b"], distance=connection["distance"])

    # Draw the graph
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1000)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color="gray")
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, font_color="black")

    # Add edge labels (distances)
    edge_labels = nx.get_edge_attributes(G, "distance")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Graph Visualization with Labels")
    plt.axis("off") # Turn off the axis
    plt.savefig('graph_visualization.png')