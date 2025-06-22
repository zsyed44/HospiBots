# gcp.py

from typing import Callable, Tuple, List, Any
import os
import json

# These would be in your project structure
from graph import Graph, Node
from navigator import Navigator

import google.generativeai as genai

class GCP:
    _do_shutdown = False

    def __init__(self, current_node: Node, graph: Graph):
        """
        Initializes the GCP instance.
        """
        self.current_node = current_node
        self.graph = graph
        self.gemini_model = None
        print("GCP module initialized.")

    def _setup_gemini(self):
        """Initialize Gemini AI with API key from environment."""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set. This bot requires Gemini AI to function.")
        
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash') # Using a common, powerful model
        print("Gemini initialized successfully.")
    
    def listen_for_command(self) -> Tuple[str, List[Any]]:
        """
        Prompts the user, gets input, and returns the parsed command from Gemini.
        """
        print('\n---') 
        print(f'Porter is currently in: {self.current_node.name}')
        print('Hi I\'m Porter! How can I help you?')
        print('You can ask me to "move to [destination]" or "shutdown".')

        user_prompt = input('What is your input: ')
        
        if not user_prompt:
            return "unknown", []
            
        return self.parse_command_with_gemini(user_prompt)

    def shutdown(self):
        """Sets the shutdown flag."""
        print("Shutdown command received.")
        self._do_shutdown = True

    def parse_command_with_gemini(self, user_input: str) -> Tuple[str, List[str]]:
        """
        Use Gemini to parse natural language input into commands and parameters.
        """
        available_destinations = self.get_available_destinations()
        current_location = self.current_node.name
        
        # This mapping helps Gemini understand common language requests
        destination_mappings = {
            "water": "room 100",
            "drinks": "room 100",
            "blankets": "room 100",
            "restroom": "room 200",
            "washroom": "room 200",
            "food": "room 310",
            "snacks": "room 310",
            "kitchen": "room 310",
            "lounge area": "room 310"
        }
        
        implied_dest_list = []
        
        for phrase, dest in destination_mappings.items():
            implied_dest_list.append(f'"{phrase}" -> "{dest}"')
        implied_dest_str = ",\n          ".join(implied_dest_list)


        prompt = f"""
        You are a navigation assistant for a bot named Porter. Parse the user's input and return a JSON response.

        Current Context:
        - Porter is operating within a hospital unit/ward.
        - Current location: "{current_location}"
        - Available destinations on this unit: {', '.join(available_destinations)}
        - Important common phrases and their implied destinations:
          {implied_dest_str}
        - Available commands: "move", "shutdown"
        
        User Input: "{user_input}"

        Parse this input and return ONLY a JSON object with this exact structure:
        {{
            "command": "move" or "shutdown" or "unknown",
            "destination": "destination_name" or null,
            "confidence": 0.0 to 1.0
        }}

        Rules:
        1. If the user wants to go somewhere, use the "move" command and specify the destination from the available list. Use the implied destinations for common phrases.
        2. If the user wants to stop, quit, or shutdown, use the "shutdown" command.
        3. If the destination is unclear, not on the available list, or if the request is not a move/shutdown command, set command to "unknown" and destination to null.
        4. Your response must be ONLY the JSON object, with no other text or formatting.

        Examples:
        - "Take me to Room 305" -> {{"command": "move", "destination": "room 310", "confidence": 0.9}}
        - "I need to go to the washroom" -> {{"command": "move", "destination": "room 200", "confidence": 0.8}}
        - "I'm done, please shut down" -> {{"command": "shutdown", "destination": null, "confidence": 1.0}}
        - "Where is the cafeteria?" -> {{"command": "unknown", "destination": null, "confidence": 0.2}}
        - "Move" -> {{"command": "move", "destination": null, "confidence": 0.6}}
        """

        try:
            response = self.gemini_model.generate_content(prompt)
            response_text = response.text.strip()
            
            if response_text.startswith('```json'):
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            
            parsed_response = json.loads(response_text)
            
            command = parsed_response.get('command', 'unknown')
            destination = parsed_response.get('destination')
            confidence = parsed_response.get('confidence', 0.0)
            
            print(f"Gemini parsed: command='{command}', destination='{destination}', confidence={confidence:.2f}")
            
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
            print(f"An error occurred during Gemini parsing: {e}")
            return "unknown", []
    
    def get_available_destinations(self) -> List[str]:
        """
        Returns a list of all node names in the graph.
        """
        return [node.name for node in self.graph.nodes.values()]