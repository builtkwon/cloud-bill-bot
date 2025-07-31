from pathlib import Path
import json
import os

CONFIG_DIR = Path(__file__).resolve().parent.parent/"config"
CONFIG_DIR.mkdir(exist_ok=True)

def config_path(guild_id: int) -> Path:
    return CONFIG_DIR / f"aws_keys_{guild_id}.json"

def store_config(guild_id: int, config: dict) -> None:
    with open(config_path(guild_id), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def retrieve_config(guild_id: int) -> dict:
    path = config_path(guild_id)
    if not path.exists():
        return{}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)