from pymongo import MongoClient

client = MongoClient("mongodb+srv://dchaud26:EasVcErqT6FSbVCD@cluster0.wgvxeqr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["porter_db"]

db.tasks.insert_many([
    { "task_id": 1, "type": "delivery", "priority": "high", "room": "301", "item": "Medical supplies", "status": "in-progress", "assignedBot": "Porter-01" },
    { "task_id": 2, "type": "scribing", "priority": "normal", "room": "205", "nurse": "Sarah Johnson", "status": "pending", "assignedBot": None },
    { "task_id": 3, "type": "comfort", "priority": "low", "room": "102", "request": "Water and snacks", "status": "queued", "assignedBot": None }
])