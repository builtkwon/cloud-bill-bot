import os
import json

CONFIG_DIR = "config"
USER_CONFIG_FILE = os.path.join(CONFIG_DIR, "user_visibility.json")

if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

if not os.path.exists(USER_CONFIG_FILE):
    with open(USER_CONFIG_FILE, "w") as f:
        json.dump({}, f)

def get_ephemeral(user_id: int) -> bool:
    with open(USER_CONFIG_FILE, "r") as f:
        data = json.load(f)
    return data.get(str(user_id), True)

def set_ephemeral(user_id: int, is_private: bool):
    with open(USER_CONFIG_FILE, "r") as f:
        data = json.load(f)
    data[str(user_id)] = is_private
    with open(USER_CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)
