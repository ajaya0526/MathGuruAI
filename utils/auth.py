import os
import json

USER_DB = 'utils/users.json'

# Ensure users.json exists
if not os.path.exists(USER_DB):
    with open(USER_DB, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(USER_DB, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, 'w') as f:
        json.dump(users, f, indent=4)

def check_login(username, password):
    users = load_users()
    return users.get(username) == password

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True
