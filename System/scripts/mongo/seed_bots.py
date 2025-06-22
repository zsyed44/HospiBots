from pymongo import MongoClient

# TODO: move to .env
client = MongoClient("mongodb+srv://dchaud26:EasVcErqT6FSbVCD@cluster0.wgvxeqr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["porter_db"]

db.bots.insert_many([
    { "bot_id": 1, "name": "Porter-01", "status": "active", "location": "Room 204", "battery": 85, "task": "Delivery to Room 301", "priority": "normal" },
    { "bot_id": 2, "name": "Porter-02", "status": "charging", "location": "Charging Station A", "battery": 45, "task": None, "priority": None },
    { "bot_id": 3, "name": "Porter-03", "status": "active", "location": "Pharmacy", "battery": 92, "task": "Prescription pickup", "priority": "high" }
])