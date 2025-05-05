# utils/history.py

import json
import os
from datetime import datetime

# Define where the history will be saved
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'history.json')

# -----------------------------
# Function to Save New History
# -----------------------------

def save_history(expression, result, hint=""):
    """
    Save a new math problem attempt into the history file.
    Stores: expression, result, hint, and timestamp.
    """

    new_entry = {
        'expression': expression,
        'result': result,
        'hint': hint,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # If file exists, load existing data
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    history.append(new_entry)

    # Save back to file
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

# -----------------------------
# Function to Load All History
# -----------------------------

def load_history():
    """
    Load and return the entire history of math problems attempted.
    Returns an empty list if no history exists.
    """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

