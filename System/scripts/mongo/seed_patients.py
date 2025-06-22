from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# TODO: move to .env
client = MongoClient(os.environ.get("MONGODB_URI"))
db = client["porter_db"]

db.patients.insert_many([
    { "patient_id": 1, "first_name": "Jorjor", "last_name": "Well", "notes": "N/A"},
    { "patient_id": 2, "first_name": "Phil", "last_name": "Phil", "notes": "Diabetic"},
    { "patient_id": 3, "first_name": "John", "last_name": "Doe", "notes": "Missing"}
])