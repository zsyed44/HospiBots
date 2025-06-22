from typing import Callable, Tuple, List, Any, Optional

from navigator import Navigator
from graph import Graph, Node
import os
import json

import google.generativeai as genai

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
        
        self._setup_gemini()  # Initialize Gemini AI 
    
    def shutdown(self):
        self._do_shutdown = True

    def move_to_next_node(self, next_node_name: Optional[str] = None) -> None:
        """
        Moves from the current node to the next node.
        The next node must be a neighbor node of the current node.
        """
        print(f'Porter is currently in: {self.current_node.name}') # Updated from "Starting at room"
        
        if next_node_name is None:
            print("I couldn't determine a specific destination from your request. Please try again with a clear location or item request.")
            return

        try:
            next_node: Node = self.graph.find_node(next_node_name)
        except Exception: 
            print(f'I\'m sorry, I don\'t recognize "{next_node_name}". Please provide a valid location on the unit/ward.')
            return 
        
        path = self.navigator.determine_path(self.graph, self.current_node, next_node) # using the Navigator to find the path
        
        if not path:
            print(f"I cannot find a path from {self.current_node.name} to {next_node.name}. Please try a different location or check the map.")
            return

        print(f'Calculating shortest path from {self.current_node.name} to {next_node.name}: {[node.name for node in path]}')

        # Move
        for node in path:
            self.walk_to_sister_node(node)
        
        self.current_node = next_node # Update current node after moving
        print(f"Successfully arrived at {self.current_node.name}")

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

            if command: 
                try:
                    if params:
                        command(*params) 
                    else: 
                        command()
                except TypeError as e:
                    print(f"Error executing command '{command.__name__}' with params {params}. Error: {e}")
                    print("This might happen if the command expects different arguments than provided.")
                except Exception as e: # Catch any other errors during command execution
                    print(f"An unexpected error occurred during command '{command.__name__}' execution: {e}")
            else:
                # This block is executed if listen_for_command returned (None, None)
                print("I didn't understand that command. Please try again.")

            # raise NotImplementedError

    def listen_for_command(self) -> Tuple[Callable[..., Any] | None, List[Any] | None]:
        print('\n---') # Added separator for readability
        print(f'Porter is currently in: {self.current_node.name}') # Added current location feedback
        print('Hi I\'m Porter! How can I help?')
        print('You can ask me to "move to [destination]" (e.g., "move to kitchen") or "shutdown".')

        user_prompt = input('What is your input: ')
        
        # Use Gemini to parse the user's prompt
        command_str, params = self.parse_command_with_gemini(user_prompt)
        
        if command_str == 'move':
            return self.move_to_next_node, params 
        elif command_str == 'shutdown':
            return self.shutdown, []
        else:
            return None, None 
    
        # user_prompt = listen_to_user()
        # command: str = gemini.parse_prompt(user_prompt)
        
        # if command == 'shutdown':
        #     return (self.shutdown, None)    
        # params = gemini.extract_params(user_prompt)
        # return (command, params)
    
    def _setup_gemini(self):
        """Initialize Gemini AI with API key from environment."""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set. This bot requires Gemini AI to function.")
        
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        print("Gemini initialized")
    
    def parse_command_with_gemini(self, user_input: str) -> Tuple[str, List[str]]:
        """
        Use Gemini to parse natural language input into commands and parameters.
        """
        available_destinations = self.get_available_destinations()
        current_location = self.current_node.name
        
        destination_mappings = {
            "water": "Supply Closet",
            "drinks": "Supply Closet",
            "blankets": "Supply Closet",
            "restroom": "Patient Washroom",
            "washroom": "Patient Washroom",
            "food": "Lounge Area",
            "snacks": "Lounge Area",
            "kitchen": "Lounge Area" # If "kitchen" means the same as "Lounge Area"
        }
        
        prompt_destinations = available_destinations[:] # Copy the list
        for alias, actual_dest in destination_mappings.items():
            if actual_dest in available_destinations and alias not in prompt_destinations:
                prompt_destinations.append(f"{actual_dest} (e.g., '{alias}')")
        # Create a detailed prompt for Gemini
        prompt = f"""
        You are a navigation assistant for a bot named Porter. Parse the user's input and return a JSON response.

        Current Context:
        - Porter is operating within a hospital unit/ward.
        - Current location: {current_location}
        - Available destinations on this unit: {', '.join(available_destinations)}
        - Important common phrases and their implied destinations:
          - "water", "drinks", "blankets" -> "Supply Closet"
          - "restroom", "washroom" -> "Patient Washroom"
          - "food", "snacks", "kitchen" -> "Lounge Area"
        - Available commands: "move", "shutdown"
        User Input: "{user_input}"

        Parse this input and return ONLY a JSON object with this exact structure:
        {{
            "command": "move" or "shutdown",
            "destination": "destination_name" or null,
            "confidence": 0.0 to 1.0,
        }}

        Rules:
        1. If user wants to go somewhere, use "move" command and specify the destination
        2. If user wants to stop/quit/shutdown, use "shutdown" command
        3. Only use destinations from the available list
        4. If destination is unclear or not available, set destination to null (also can be used by calling move_to_next_node without params)
        5. Return ONLY the JSON object, no other text

        Examples (hospital-specific):
        - "Take me to Room 305" → {{"command": "move", "destination": "Room 305", "confidence": 0.9}}
        - "Go to the Nurses' Station" → {{"command": "move", "destination": "Nurses' Station", "confidence": 0.8}}
        - "Porter, proceed to the Medication Room" → {{"command": "move", "destination": "Medication Room", "confidence": 0.95}}
        - "Can you bring me some blankets?" → {{"command": "unknown", "destination": null, "confidence": 0.2}}
        - "Where is the X-Ray department?" → {{"command": "unknown", "destination": null, "confidence": 0.1}}
        - "I need to go to the washroom" → {{"command": "move", "destination": "Patient Washroom", "confidence": 0.7}}
        - "I'm done for the day, shut down" → {{"command": "shutdown", "destination": null, "confidence": 1.0}}
        - "Move" → {{"command": "move", "destination": null, "confidence": 0.6}}
        """

        try:
            response = self.gemini_model.generate_content(prompt)
            
            # Parse the JSON response
            response_text = response.text.strip()
            
            # Remove any markdown formatting if present
            if response_text.startswith('```json'):
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif response_text.startswith('```'):
                response_text = response_text.split('```')[1].strip()
            
            parsed_response = json.loads(response_text)
            
            command = parsed_response.get('command', 'unknown')
            destination = parsed_response.get('destination')
            confidence = parsed_response.get('confidence', 0.0)
            
            print(f"Gemini parsed: '{user_input}' → command: '{command}'" + 
                  (f", destination: '{destination}'" if destination else "") + 
                  f" (confidence: {confidence:.1f})")
            
            # Return command and parameters
            if command == "move":
                return command, [destination] 
            elif command == "shutdown":
                return command, []
            else:
                return "unknown", []
                
        except json.JSONDecodeError as e:
            print(f"⚠ Failed to parse Gemini response as JSON: {e}. Raw response: '{response.text}'")
            return "unknown", []
        except Exception as e:
            print(f"An error occurred during Gemini parsing: {e}. User input: '{user_input}'")
            return "unknown", []
    
    def get_available_destinations(self) -> List[str]:
        """
        for simplicity, we'll list all nodes in the graph.
        """
        # Ensure that graph.nodes is a dict of Node objects or similar
        return [node.name for node in self.graph.nodes]
    
if __name__ == "__main__":
    # --- Create a sample Graph for a Hospital Unit/Ward ---
    ward_graph = Graph()

    node_data = [
        (1, "Room 301"),
        (2, "Room 302"),
        (3, "Nurses' Station"),
        (4, "Medication Room"),
        (5, "Supply Closet"),
        (6, "Patient Washroom"),
        (7, "Lounge Area"),
        (8, "North Hallway"),
        (9, "South Hallway")
    ]

    nodes_by_id = {} # A temporary dict to easily get nodes by ID for adding edges
    for node_id, node_name in node_data:
        ward_graph.create_node(node_id, node_name)
        nodes_by_id[node_id] = ward_graph.get_node(node_id) # Get the created Node object

    
    nodes_by_id[3].add_neighbor(nodes_by_id[8], 1.0) # Nurses' Station <-> North Hallway
    nodes_by_id[8].add_neighbor(nodes_by_id[3], 1.0)

    nodes_by_id[3].add_neighbor(nodes_by_id[9], 1.0) # Nurses' Station <-> South Hallway
    nodes_by_id[9].add_neighbor(nodes_by_id[3], 1.0)

    nodes_by_id[8].add_neighbor(nodes_by_id[1], 1.0) # North Hallway <-> Room 301
    nodes_by_id[1].add_neighbor(nodes_by_id[8], 1.0)

    nodes_by_id[8].add_neighbor(nodes_by_id[2], 1.0) # North Hallway <-> Room 302
    nodes_by_id[2].add_neighbor(nodes_by_id[8], 1.0)

    nodes_by_id[8].add_neighbor(nodes_by_id[4], 1.0) # North Hallway <-> Medication Room
    nodes_by_id[4].add_neighbor(nodes_by_id[8], 1.0)

    nodes_by_id[9].add_neighbor(nodes_by_id[5], 1.0) # South Hallway <-> Supply Closet
    nodes_by_id[5].add_neighbor(nodes_by_id[9], 1.0)

    nodes_by_id[9].add_neighbor(nodes_by_id[6], 1.0) # South Hallway <-> Patient Washroom
    nodes_by_id[6].add_neighbor(nodes_by_id[9], 1.0)

    nodes_by_id[9].add_neighbor(nodes_by_id[7], 1.0) # South Hallway <-> Lounge Area
    nodes_by_id[7].add_neighbor(nodes_by_id[9], 1.0)

    starting_node = ward_graph.get_node(3)
    try:
        porter_bot = Bot(id="Porter-WardBot-001", graph=ward_graph, starting_node=starting_node)
        porter_bot.run()
    except ValueError as e:
        print(f"Bot initialization failed: {e}")
        print("Please ensure your GOOGLE_API_KEY is correctly set in your environment variables.")
    except Exception as e:
        print(f"An unexpected error occurred during bot execution: {e}")
