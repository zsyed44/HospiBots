from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# MongoDB Atlas connection
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise RuntimeError("Missing MONGODB_URI in environment variables")

client = MongoClient(MONGODB_URI)
db = client["porter_db"]  # Replace with your actual database name

@app.route("/api/bots", methods=["GET"])
def get_bots():
    bots = list(db.bots.find({}, {'_id': 0}))  # Exclude internal _id field
    return jsonify(bots)

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = list(db.tasks.find({}, {'_id': 0}))
    return jsonify(tasks)

# Define the path to the graph file
GRAPH_FILE = "graph.json"

@app.route("/api/graph", methods=["GET"])
def get_graph():
    """
    Retrieves the graph data from 'graph.json'.
    If the file does not exist, an empty JSON object is returned.
    """
    if not os.path.exists(GRAPH_FILE):
        # If the graph file doesn't exist, return an empty graph
        print(f"Graph file '{GRAPH_FILE}' not found. Returning empty graph.")
        return jsonify({}), 200
    
    try:
        with open(GRAPH_FILE, "r") as f:
            graph_data = json.load(f)
        print(f"Successfully loaded graph from '{GRAPH_FILE}'.")
        return jsonify(graph_data), 200
    except json.JSONDecodeError:
        # Handle cases where the file exists but is not valid JSON
        print(f"Error decoding JSON from '{GRAPH_FILE}'. File might be corrupted.")
        return jsonify({"error": "Invalid JSON format in graph file"}), 500
    except IOError as e:
        # Handle other I/O errors (e.g., permission issues)
        print(f"Error reading file '{GRAPH_FILE}': {e}")
        return jsonify({"error": f"Could not read graph file: {e}"}), 500

@app.route("/api/graph", methods=["POST"])
def post_graph():
    """
    Receives graph data as JSON in the request body and overwrites
    the 'graph.json' file with this new data.
    """
    if not request.is_json:
        # Ensure the request content type is application/json
        print("Request content type is not application/json.")
        return jsonify({"error": "Request must be JSON"}), 400

    graph_data = request.get_json()
    
    if graph_data is None:
        # Handle cases where get_json() returns None (e.g., malformed JSON)
        print("Received malformed JSON data.")
        return jsonify({"error": "Malformed JSON data"}), 400

    try:
        with open(GRAPH_FILE, "w") as f:
            json.dump(graph_data, f, indent=4) # Use indent for pretty printing
        print(f"Successfully saved graph to '{GRAPH_FILE}'.")
        return jsonify({"message": "Graph saved successfully"}), 200
    except IOError as e:
        # Handle I/O errors during writing
        print(f"Error writing to file '{GRAPH_FILE}': {e}")
        return jsonify({"error": f"Could not write graph file: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)
