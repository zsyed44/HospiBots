from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys
import json
import ssl

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BOT_SRC_PATH = os.path.join(BASE_DIR, 'bot', 'src')
sys.path.insert(0, BOT_SRC_PATH)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access (important for React)

# --- MongoDB Atlas Connection ---
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    # Use a more descriptive error message and exit if critical env var is missing
    print("Error: MONGODB_URI environment variable not set. Please add it to your .env file.")
    sys.exit(1) # Exit the application if essential configuration is missing

try:
    client = MongoClient(
        MONGODB_URI,
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE,
        ssl_version=ssl.PROTOCOL_TLSv1_2,
    )
    
    db = client["porter_db"]  # Replace with your actual database name
    # Optional: Test connection to MongoDB
    client.admin.command('ping')
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1) # Exit if cannot connect to DB

# --- API Endpoints ---

@app.route("/api/bots", methods=["GET"])
def get_bots():
    """Fetches bot data from MongoDB."""
    # Ensure MongoDB operations handle potential errors gracefully
    try:
        bots = list(db.bots.find({}, {'_id': 0}))  # Exclude internal _id field
        return jsonify(bots)
    except Exception as e:
        print(f"Error fetching bots from MongoDB: {e}")
        return jsonify({"error": "Failed to fetch bot data"}), 500

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Fetches task data from MongoDB."""
    try:
        tasks = list(db.tasks.find({}, {'_id': 0}))
        return jsonify(tasks)
    except Exception as e:
        print(f"Error fetching tasks from MongoDB: {e}")
        return jsonify({"error": "Failed to fetch task data"}), 500

@app.route('/api/bot_status', methods=['GET'])
def get_bot_status():
    """Returns the current status of the bot (location, shutdown state)."""
    if porter_bot is None:
        return jsonify({"error": "Bot not initialized"}), 500
    
    # You might want to expand this to include more details from the bot object
    # For now, we fetch location directly from the bot instance
    return jsonify({
        "id": porter_bot.id,
        "location": porter_bot.current_node.name if porter_bot.current_node else "Unknown",
        "is_listening_enabled": porter_bot.voice_recorder.speech_enabled, # Reflects if STT is enabled (backend)
        "is_shutdown": porter_bot.gcp._do_shutdown # Reflects if bot is logically shutting down
    })

@app.route('/api/command', methods=['POST'])
def handle_command():
    if porter_bot is None:
        return jsonify({"error": "Bot not initialized"}), 500

    data = request.get_json()
    command_text = data.get('commandText', '').strip()
    if not command_text:
        return jsonify({"status": "error", "message": "No command text provided."}), 400

    # Prepare a buffer to capture all prints
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        # Echo the terminal-style prompt
        print(f"Porter is currently in: {porter_bot.current_node.name}")
        print("Hi I'm Porter! How can I help you?")
        print('You can ask me to "move to [destination]" or "shutdown"')
        print(f"What is your input: {command_text}")

        # Parse & execute
        command, params = porter_bot.gcp.parse_command_with_gemini(command_text)
        destination = params[0] if params else None
        # show Gemini’s parse
        print(f"Gemini parsed: command={command!r}, destination={destination!r}, confidence=<n/a>")

        status = "success"
        response_message = ""
        try:
            if command == 'move':
                # move_to_room itself prints the path, execution, etc.
                result = porter_bot.move_to_room(destination)
                if result == "already_there":
                    response_message = f"Porter is already in {destination}."
                else:
                    response_message = f"Successfully arrived at {porter_bot.current_node.name}."
            elif command == 'shutdown':
                porter_bot.shutdown()
                response_message = "Porter is shutting down. Goodbye!"
                status = "shutdown_initiated"
            else:
                status = "unknown_command"
                response_message = "Sorry, I didn't understand that command. Please try again."
        except ValueError as e:
            status = "error"
            response_message = f"Navigation Error: {e}"
            print(response_message)
        except RuntimeError as e:
            status = "error"
            response_message = f"Bot Execution Error: {e}"
            print(response_message)
        except Exception as e:
            status = "error"
            response_message = f"An unexpected error occurred: {e}"
            print(response_message)

        # Final status line
        print(response_message)

    # Grab the full log
    log = buf.getvalue().splitlines()

    return jsonify({
        "status": status,
        "message": response_message,
        "bot_current_location": porter_bot.current_node.name,
        "bot_is_shutdown": porter_bot.gcp._do_shutdown,
        "log": log
    })

@app.route("/api/patients", methods=["GET"])
def get_patients():
    patients = list(db.patients.find({}, {'_id': 0}))
    return jsonify(patients)

if __name__ == "__main__":
    print("Starting Flask API server on http://127.0.0.1:3000")
    app.run(host="0.0.0.0", debug=True, port=3000)
