from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

GRAPH_FILE = 'graph.json'

def load_graph():
    if os.path.exists(GRAPH_FILE):
        with open(GRAPH_FILE, 'r') as f:
            return json.load(f)
    return {"nodes": [], "connections": []}

def save_graph(graph_data):
    with open(GRAPH_FILE, 'w') as f:
        json.dump(graph_data, f, indent=4)

@app.route('/api/v1/navgraph', methods=['GET'])
def get_graph():
    return jsonify(load_graph())

@app.route('/api/v1/navgraph', methods=['POST'])
def update_graph():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    if 'nodes' not in data or 'connections' not in data:
        return jsonify({'error': 'Graph must contain nodes and connections'}), 400
    
    save_graph(data)
    return jsonify(data), 200

# if __name__ == '__main__': for testing purposes
#     app.run(debug=True, host='0.0.0.0', port=3000)