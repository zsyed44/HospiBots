from bot import Bot

from graph import Graph, load_graph_from_json, load_graph_from_json_file

PORTER_SYSTEM_URL = 'localhost:3000'
NAVGRAPH_ENDPOINT = PORTER_SYSTEM_URL + '/api/v1/navgraph'

BACKUP_NAVGRAPH_FILE_PATH = '../data/graph.json'

def get_nav_graph() -> Graph:
    """
    Loads a nav graph for the bot.
    By default loads from server endpoint, then from backup in data dir

    Returns:
        Graph: _description_
    """

    import requests
    import json 

    try:
        # pull from endpoint
        res = requests.get(NAVGRAPH_ENDPOINT)
        response = json.loads(res.text)

        graph = load_graph_from_json(response)
    except requests.exceptions.RequestException:
        print(f'Failed to pull navgraph from PortSys, falling back to local navgraph in {BACKUP_NAVGRAPH_FILE_PATH}')
    
        # just read from file
        graph = load_graph_from_json_file(BACKUP_NAVGRAPH_FILE_PATH)

    return graph

def main():
    # Get graph
    graph = get_nav_graph()

    # initialize self
    # bot = Bot(graph, starting_node, starting_orientation)
    bot = Bot('PORTER', graph, graph.get_one_node())

    bot.run()

if __name__ == '__main__':
    main()