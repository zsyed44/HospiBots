from typing import Callable, List, Any
import json
from navigator import Navigator
from graph import Graph, Node

class Bot:
    def __init__(self, id: str, graph: Graph, starting_node: Node) -> None:
        # Set given params
        self.id = id
        self.graph = graph
        self.current_node = starting_node

        # Set navigator
        self.navigator = Navigator()
        self.path_to_destination: List[Node] = [] # Stores the planned path

        self.possible_commands = [
            "move to <room_name>",
            "shutdown",
        ]

        self.command_map: dict[str, Callable[..., Any]] = { # type: ignore
            "move to": self.move_to_room,
            "shutdown": self.shutdown
        }

    def shutdown(self):
        print("Bot shutting down...")
        exit() # Exits the program

    def start(self):
        """
        Bots when ran, start and wait for input.
        On input, they enter a command, and execute that command
        """
        print(f"Bot {self.id} started at {self.current_node.name}.")
        while True:
            self.listen_for_command()

    def listen_for_command(self):
        print('\n--- Hi I\'m Porter! How can I help? ---')
        print('Enter a command from these options:')
        for cmd in self.possible_commands:
            print(f"- {cmd}")

        user_input = input('Your command: ').strip().lower()

        # Simple command parsing
        command_found = False
        for cmd_prefix, func in self.command_map.items():
            if user_input.startswith(cmd_prefix):
                # Extract the argument (e.g., room name for "move to")
                arg = user_input[len(cmd_prefix):].strip()

                if arg:
                    func(arg)
                else:
                    func()
                    
                command_found = True
                break

        if not command_found:
            print("Sorry, I didn't understand that command. Please try again.")

    def move_to_room(self, room_name: str):
        """
        Navigates the bot to the specified room using Dijkstra's algorithm.
        """
        destination_node = self.graph.get_node_by_name(room_name)

        if not destination_node:
            print(f"Room '{room_name}' not found. Please check the room name.")
            return

        if self.current_node == destination_node:
            print(f"I'm already in {destination_node.name}!")
            return

        print(f"Calculating path from {self.current_node.name} to {destination_node.name}...")
        path = self.navigator.find_shortest_path(self.graph, self.current_node, destination_node)

        if path:
            self.path_to_destination = path
            print("Path found:")
            for i, node in enumerate(path):
                print(f"{i+1}. {node.name}")

            self._execute_path()
            self.current_node = destination_node # Update current location after path execution
            print(f"Successfully arrived at {self.current_node.name}.")
        else:
            print(f"Could not find a path from {self.current_node.name} to {destination_node.name}.")

    def _execute_path(self):
        """
        Simulates moving along the planned path.
        In a real application, this would involve more complex actions (e.g., controlling motors).
        """
        if not self.path_to_destination:
            print("No path planned to execute.")
            return

        print("\nExecuting path...")
        # Start from the second node in the path, as the first is the current_node
        for i in range(1, len(self.path_to_destination)):
            prev_node = self.path_to_destination[i-1]
            next_node = self.path_to_destination[i]
            # Here you would add logic for actual movement
            print(f"Moving from {prev_node.name} to {next_node.name}...")
            # Simulate time taken based on distance if needed
        print("Path execution complete.")
        self.path_to_destination = [] # Clear the path after execution

    def move_to_next_node(self):
        """
        Placeholder for moving to the next node in a pre-planned path,
        or just directly connected node for simple debugging.
        This is not used by the `move_to_room` command directly, which plans the full path.
        """
        print("This command is handled by 'move to <room_name>'.")
        # Example of direct move if a path isn't planned:
        # if self.graph.get_neighbors(self.current_node):
        #     next_node_info = self.graph.get_neighbors(self.current_node)[0]
        #     self.current_node = next_node_info['node']
        #     print(f"Moved to {self.current_node.name}")
        # else:
        #     print("No direct neighbors to move to.")

# --- Main execution to test the Bot ---
if __name__ == "__main__":
    json_data = """
    {
        "nodes": [
            {
                "id": 0,
                "name": "service room"
            },
            {
                "id": 1,
                "name": "room 100"
            },
            {
                "id": 2,
                "name": "room 200"
            },
            {
                "id": 3,
                "name": "room 220"
            },
            {
                "id": 4,
                "name": "room 310"
            },
            {
                "id": 5,
                "name": "room 550"
            }
        ],
        "connections": [
            {
                "node_a": 0,
                "node_b": 1,
                "distance": 5
            },
            {
                "node_a": 1,
                "node_b": 2,
                "distance": 5
            },
            {
                "node_a": 3,
                "node_b": 4,
                "distance": 5
            },
            {
                "node_a": 4,
                "node_b": 5,
                "distance": 5
            },
            {
                "node_a": 5,
                "node_b": 2,
                "distance": 5
            },
            {
                "node_a": 1,
                "node_b": 4,
                "distance": 5
            }
        ]
    }
    """

    # 1. Parse JSON data and build the Graph
    data = json.loads(json_data)
    my_graph = Graph()

    for node_data in data['nodes']:
        my_graph.add_node(node_data['id'], node_data['name'])

    for conn_data in data['connections']:
        my_graph.add_connection(conn_data['node_a'], conn_data['node_b'], conn_data['distance'])

    # 2. Initialize the Bot
    starting_node_id = 0 # Start at "service room"
    starting_node = my_graph.get_node_by_id(starting_node_id)

    if starting_node:
        porter_bot = Bot(id="Porter-001", graph=my_graph, starting_node=starting_node)
        porter_bot.start()
    else:
        print("Error: Starting node not found.")