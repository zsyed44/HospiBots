from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# TODO: move to .env
client = MongoClient(os.environ.get("MONGODB_URI"))
db = client["porter_db"]

db.bots.insert_many([
    { "bot_id": 1, "name": "Porter-01", "status": "active", "location": "Room 204", "battery": 85, "task": "Delivery to Room 301", "priority": "normal" },
    { "bot_id": 2, "name": "Porter-02", "status": "charging", "location": "Charging Station A", "battery": 45, "task": None, "priority": None },
    { "bot_id": 3, "name": "Porter-03", "status": "active", "location": "Pharmacy", "battery": 92, "task": "Prescription pickup", "priority": "high" }
])