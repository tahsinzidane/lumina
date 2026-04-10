import json
import os

# Store history in the user's home directory to keep it persistent
DB_FILE = os.path.expanduser("~/.lumina_history.json")

def load_history():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_command(command):
    command = command.strip()
    if not command:
        return
    
    history = load_history()
    
    # Remove existing entry to move it to the top (Most Recent)
    if command in history:
        history.remove(command)
    
    history.insert(0, command)
    
    # Keep only the last 100 commands to maintain performance
    with open(DB_FILE, "w") as f:
        json.dump(history[:100], f, indent=4)