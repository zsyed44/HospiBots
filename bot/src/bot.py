from navigator import Navigator
from graph import Graph, load_graph_from_json

SPIDER_URL = 'localhost:3000'
NAVGRAPH_ENDPOINT = SPIDER_URL + '/api/v1/navgraph'

def get_nav_graph() -> Graph:
    """
    Loads a nav graph for the bot.
    By default loads from server endpoint, then from backup in data dir

    Returns:
        Graph: _description_
    """

    import requests
    import json 

    res = requests.get(NAVGRAPH_ENDPOINT)
    response = json.loads(res.text)

    graph = load_graph_from_json(response)

    return graph
    

class Bot:
    do_shutdown = False

    def __init__(self) -> None:
        # pull the navgraph
        self.graph = get_nav_graph()

        # Set navigator
        self.navigator = Navigator()

    def run(self):
        """
        Bots when ran, start and wait for input.
        On input, they enter a command, and execute that command
        """

        while True:
            # Stop if the bot has had a shutdown command
            if self.do_shutdown:
                break

            command, params = self.listen_for_command() # type: ignore

            raise NotImplementedError

    def listen_for_command(self) -> tuple[function, list[str]]: # type: ignore
        raise NotImplementedError