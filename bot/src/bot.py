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
        print("Bot shutting down...")
        exit() # Exits the program

    def start(self):
        """
        Bots when ran, start and wait for input.
        On input, they enter a command, and execute that command
        """
        print(f"Bot {self.id} started at {self.current_node.name}.")
        while not self.gcp._do_shutdown:
            # IMPORTANT: Update GCP with the bot's current location before listening.
            self.gcp.current_node = self.current_node

            # Get the parsed command from the GCP module.
            if hasattr(self, "_get_user_input_from_source"):
                user_input = self._get_user_input_from_source()
            else:
                user_input = self.gcp.listen_for_command()

            # Pass the user input to GCP for Gemini parsing
            command, params = self.gcp.parse_command_with_gemini(user_input)
            # Execute actions based on the parsed command.
            if command == 'move':
                # Check if a destination was provided.
                if params and params[0] is not None:
                    self.move_to_room(params[0])
                else:
                    print("I'm ready to move, but you need to provide a destination.")
            
            elif command == 'shutdown':
                self.shutdown()

            elif command == 'unknown':
                print("Sorry, I didn't understand that command. Please try again.")

    def _get_user_input_from_source(self) -> str:
        """
        Provides a choice between typing and speaking,
        and retrieves input accordingly.
        """
        if self.voice_recorder.speech_enabled:
            # Loop until valid input (typed or spoken) is received
            while True:
                choice = input('Type command or press V for voice: ').strip().lower()
                
                if choice == 'v':
                    spoken_text = self.voice_recorder.record_command()
                    if spoken_text:
                        return spoken_text
                    else:
                        print("Voice input failed or no speech detected. Please try again or type.")
                else:
                    return choice # Return typed input directly
        else:
            # If speech is not enabled, always fallback to typed input
            return input('Your command: ').strip().lower()

    """
    def listen_for_command(self):
        print('\n--- Hi I\'m Porter! How can I help? ---')
        print('Enter a command from these options:')
        for cmd in self.possible_commands:
            print(f"- {cmd}")

        user_input = input('Your command: ').strip().lower() # this is where the text to speech would be used

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
    """
    
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
    # Ensure you have these files in the correct relative paths
    try:
        with open("../bot/data/graph.json") as f:
            data = json.load(f)

        my_graph = Graph()

        for node_data in data['nodes']:
            my_graph.add_node(node_data['id'], node_data['name'])

        for conn_data in data['connections']:
            my_graph.add_connection(conn_data['node_a'], conn_data['node_b'], conn_data['distance'])

        starting_node_id = 0 # Start at the first node in the graph data
        starting_node = my_graph.get_node_by_id(starting_node_id)

        if starting_node:
            porter_bot = Bot(id="Porter-001", graph=my_graph, starting_node=starting_node)
            porter_bot.start()
        else:
            print(f"Error: Starting node with ID {starting_node_id} not found.")

    except FileNotFoundError:
        print("Error: `data/graph.json` not found. Please ensure the graph data file exists.")
    except ImportError as e:
        print(f"Error: A required module is missing. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")