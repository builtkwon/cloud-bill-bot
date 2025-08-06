from infra.memory_config import retrieve_config

def get_current_region(guild_id: int) -> str:
    config = retrieve_config(guild_id)
    return config.get("region", "us-east-1")
