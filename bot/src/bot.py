from typing import Callable, Tuple, List, Any

from navigator import Navigator
from graph import Graph, Node

class Bot:
    _do_shutdown = False

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

        self.command_map: dict[str, Callable[..., Any]] = { # type: ignore
            "move": self.move_to_next_node,
            "shutdown": self.shutdown
        }
    
    def shutdown(self):
        self._do_shutdown = True

    def move_to_next_node(self) -> None:
        """
        Moves from the current node to the next node.
        The next node must be a neighbor node of the current node.

        """
        print(f'Starting at room {self.current_node.name}')
        next_node_name = input('Which next node?')

        try:
            next_node: Node = self.graph.find_node(next_node_name)
        except Exception:
            print('I\'m sorry I don\'t know what that is? Are you sure that\'s a node?')
            return 
        
        path = self.navigator.determine_path(self.graph, self.current_node, next_node)
        print(f'Path from {self.current_node} to {next_node}: {path}')

        # Move
        for node in path:
            self.walk_to_sister_node(node)

    def walk_to_sister_node(self, node: Node):
        print(f'moving to {node.name}')

    def run(self):
        """
        Bots when ran, start and wait for input.
        On input, they enter a command, and execute that command
        """

        while True:
            # Stop if the bot has had a shutdown command
            if self._do_shutdown:
                break

            command, params = self.listen_for_command()

            if not params:
                command()
            else:
                command(params)

            # raise NotImplementedError

    def listen_for_command(self) -> Tuple[Callable[..., Any], List[Any] | None]: # type: ignore
        # TEMPORARY MANUAL SOLUTION
        # WILL BE REPLACED WITH GEMINI SOLUTION
        print('Hi I\'m Porter! How can I help?')
        print('Enter a command from these options')

        # print command options
        for command in self.command_map.keys(): # type: ignore
            print(f' - {command}')

        command_selection = input('What is your input: ')
        command: Callable[..., Any] = self.command_map[command_selection]
        
        return (command, None)