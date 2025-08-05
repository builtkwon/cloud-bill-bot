import os
import json
from pathlib import Path
from functools import lru_cache
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent / "config"

DEFAULT_CONFIG = {
    "ephemeral": True
}

def _get_config_path(user_id: int) -> Path:
    return BASE_DIR / f"user_{user_id}.json"

def _log_change(user_id: int, key: str, value):
    log_path = BASE_DIR / "user_config.log"
    timestamp = datetime.now().isoformat()
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] User {user_id} set {key} = {value}\n")

def get_user_config(user_id: int) -> dict:
    config_path = _get_config_path(user_id)
    try:
        if not config_path.exists():
            return DEFAULT_CONFIG.copy()
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG.copy()
    
def set_user_config(user_id: int, config: dict):
    config_path = _get_config_path(user_id)
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

@lru_cache(maxsize=1000)
def get_ephemeral(user_id: int) -> bool:
    return get_user_config(user_id).get("ephemeral", True)

def set_ephemeral(user_id: int, value: bool):
    config = get_user_config(user_id)
    config["ephemeral"] = value
    set_user_config(user_id, config)
    _log_change(user_id,"ephemeral", value)
    get_ephemeral.cache_clear()