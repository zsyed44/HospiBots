from flask import Flask, jsonify, request  # Add request import!
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, methods=['GET', 'POST', 'OPTIONS'])

# MongoDB Atlas connection
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise RuntimeError("Missing MONGODB_URI in environment variables")

client = MongoClient(MONGODB_URI)
db = client["porter_db"]

@app.route("/api/bots", methods=["GET"])
def get_bots():
    bots = list(db.bots.find({}, {'_id': 0}))
    return jsonify(bots)

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = list(db.tasks.find({}, {'_id': 0}))
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def create_task():
    try:
        task_data = request.get_json()
        
        highest_task = db.tasks.find_one(sort=[("task_id", -1)])
        next_task_id = (highest_task['task_id'] + 1) if highest_task else 1

        new_task = {
            'task_id': next_task_id,
            'type': task_data['type'],
            'priority': task_data['priority'],
            'room': task_data['room'],
            'status': 'pending',
            'assignedBot': None
        }

        db.tasks.insert_one(new_task)
        new_task.pop('_id', None)
        
        return jsonify(new_task), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)