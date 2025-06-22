from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = MongoClient(os.environ.get("MONGODB_URI"))
db = client["porter_db"]

# Optional: clear old data (if you're reseeding)
db.patients.delete_many({})

# Insert new patient data
db.patients.insert_many([
    {
        "id": "P-2024-001",
        "name": "Sarah Johnson",
        "age": 45,
        "gender": "Female",
        "room": "301A",
        "bed": "A",
        "admissionDate": "2024-06-20",
        "status": "stable",
        "condition": "Hypertension",
        "doctor": "Dr. Smith",
        "allergies": ["Penicillin", "Shellfish"],
        "vitals": {
            "bloodPressure": "145/90",
            "heartRate": "72 bpm",
            "temperature": "98.6°F",
            "oxygenSat": "98%",
            "lastUpdated": "2024-06-22 14:30"
        },
        "medications": ["Lisinopril 10mg", "Metformin 500mg"],
        "phone": "(555) 123-4567",
        "emergencyContact": "John Johnson - (555) 123-4568",
        "insurance": "Blue Cross Blue Shield",
        "notes": "Patient responding well to treatment. Blood pressure improving.",
        "riskLevel": "low"
    },
    {
        "id": "P-2024-002",
        "name": "Michael Chen",
        "age": 62,
        "gender": "Male",
        "room": "205B",
        "bed": "B",
        "admissionDate": "2024-06-21",
        "status": "critical",
        "condition": "Chest Pain - Rule out MI",
        "doctor": "Dr. Williams",
        "allergies": ["None known"],
        "vitals": {
            "bloodPressure": "160/95",
            "heartRate": "85 bpm",
            "temperature": "99.1°F",
            "oxygenSat": "95%",
            "lastUpdated": "2024-06-22 13:45"
        },
        "medications": ["Aspirin 81mg", "Atorvastatin 40mg", "Metoprolol 25mg"],
        "phone": "(555) 234-5678",
        "emergencyContact": "Lisa Chen - (555) 234-5679",
        "insurance": "Medicare",
        "notes": "Cardiology consult scheduled. Monitoring cardiac enzymes.",
        "riskLevel": "high"
    },
    {
        "id": "P-2024-003",
        "name": "Emma Davis",
        "age": 28,
        "gender": "Female",
        "room": "412C",
        "bed": "C",
        "admissionDate": "2024-06-21",
        "status": "recovering",
        "condition": "Pneumonia",
        "doctor": "Dr. Johnson",
        "allergies": ["Sulfa drugs"],
        "vitals": {
            "bloodPressure": "120/80",
            "heartRate": "68 bpm",
            "temperature": "100.2°F",
            "oxygenSat": "96%",
            "lastUpdated": "2024-06-22 12:00"
        },
        "medications": ["Amoxicillin 500mg", "Albuterol inhaler"],
        "phone": "(555) 345-6789",
        "emergencyContact": "Mark Davis - (555) 345-6790",
        "insurance": "Aetna",
        "notes": "Fever decreasing. Chest X-ray shows improvement.",
        "riskLevel": "medium"
    },
    {
        "id": "P-2024-004",
        "name": "Robert Wilson",
        "age": 78,
        "gender": "Male",
        "room": "108A",
        "bed": "A",
        "admissionDate": "2024-06-22",
        "status": "stable",
        "condition": "Post-operative monitoring",
        "doctor": "Dr. Brown",
        "allergies": ["Latex", "Codeine"],
        "vitals": {
            "bloodPressure": "135/85",
            "heartRate": "70 bpm",
            "temperature": "98.8°F",
            "oxygenSat": "97%",
            "lastUpdated": "2024-06-22 15:00"
        },
        "medications": ["Morphine 5mg PRN", "Docusate 100mg"],
        "phone": "(555) 456-7890",
        "emergencyContact": "Margaret Wilson - (555) 456-7891",
        "insurance": "Medicare + Supplement",
        "notes": "Post-op day 1. Incision site clean and dry. Pain controlled.",
        "riskLevel": "medium"
    }
])
