# bot/src/bot.py

from typing import Callable, List, Any
import json
from navigator import Navigator
from graph import Graph, Node
from gcp import GCP
from speech_recognizer import SimpleVoiceRecorder

class Bot:
    def __init__(self, id: str, graph: Graph, starting_node: Node) -> None:
        # Set given params
        self.id = id
        self.graph = graph
        self.current_node = starting_node

        # Set navigator
        self.navigator = Navigator()
        self.path_to_destination: List[Node] = [] # Stores the planned path
       
        self.gcp = GCP(self.current_node, self.graph)
        self.gcp._setup_gemini() # Setup Gemini AI

        self.voice_recorder = SimpleVoiceRecorder() 
        
        self.command_map: dict[str, Callable[..., Any]] = { # type: ignore
            "move to": self.move_to_room,
            "shutdown": self.shutdown
        }

    def shutdown(self):
        print("Bot shutting down signal received.")
        self.gcp._do_shutdown = True # Signal the bot to logically shut down

    # The `start` method with the input loop is removed, as control comes from the API.
    # The `_get_user_input_from_source` method is also removed, as input is received via API.

    def move_to_room(self, room_name: str):
        """
        Navigates the bot to the specified room using Dijkstra's algorithm.
        """
        destination_node = self.graph.get_node_by_name(room_name)

        if not destination_node:
            print(f"Room '{room_name}' not found. Please check the room name.")
            raise ValueError(f"Room '{room_name}' not found.") # Raise error for API to catch
            # return # Removed return, now raising exception

        if self.current_node == destination_node:
            print(f"I'm already in {destination_node.name}!")
            return "already_there" # Indicate to API that bot is already there

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
            return "success"
        else:
            print(f"Could not find a path from {self.current_node.name} to {destination_node.name}.")
            raise RuntimeError(f"Could not find path to {destination_node.name}.") # Raise error for API

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
        print("Path execution complete.")
        self.path_to_destination = [] # Clear the path after execution

    # The `move_to_next_node` method is commented out as it's not used by this flow
    # def move_to_next_node(self):
    #     """
    #     Placeholder for moving to the next node in a pre-planned path,
    #     or just directly connected node for simple debugging.
    #     This is not used by the `move_to_room` command directly, which plans the full path.
    #     """
    #     print("This command is handled by 'move to <room_name>'.")

# Removed the `if __name__ == "__main__":` block as the bot is now started by the Flask app.
# Ensure your graph.json is accessible via the path in app.py
