from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
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

@app.route("/api/patients", methods=["GET"])
def get_patients():
    patients = list(db.patients.find({}, {'_id': 0}))
    return jsonify(patients)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
