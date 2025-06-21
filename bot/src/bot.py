from typing import Callable, Tuple, List, Any

from navigator import Navigator
from graph import Graph, Node

class Bot:
    do_shutdown = False

    CommandFunction = Callable[..., Any]
    possible_commands: List[CommandFunction]

    def __init__(self, id: str, graph: Graph, starting_node: Node) -> None:
        # Set given params
        self.id = id 

        # pull the navgraph
        self.graph = graph
        self.current_node = starting_node

        # Set navigator
        self.navigator = Navigator()

        self.possible_commands = [
            self.move_to_next_node,
        ]

        self.command_map = {
            "move": self.move_to_next_node,
        }

    def move_to_next_node(self, next_node: Node) -> None:
        """
        Moves from the current node to the next node.
        The next node must be a neighbor node of the current node.

        Args:
            next_node (Node): _description_
        """
        raise NotImplementedError

    def run(self):
        """
        Bots when ran, start and wait for input.
        On input, they enter a command, and execute that command
        """

        while True:
            # Stop if the bot has had a shutdown command
            if self.do_shutdown:
                break

            command, params = self.listen_for_command() 

            command(params)

            raise NotImplementedError

    def listen_for_command(self) -> Tuple[Callable[..., Any], List[Any]]: # type: ignore
        # TEMPORARY MANUAL SOLUTION
        # WILL BE REPLACED WITH GEMINI SOLUTION
        print('Hi I\'m Porter! How can I help?')
        print('Enter a command from these options')
        print(self.command_map.keys())