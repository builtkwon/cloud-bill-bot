import os
import json

CONFIG_DIR = "config"

def get_config_path(guild_id: int) -> str:
    return os.path.join(CONFIG_DIR, f"{guild_id}.json")

def retrieve_config(guild_id: int) -> dict | None:
    path = get_config_path(guild_id)
    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

def store_config(guild_id: int, config: dict):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    path = get_config_path(guild_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
