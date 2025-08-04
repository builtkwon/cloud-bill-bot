import boto3
from utils.memory_config import retrieve_config
from utils.crypto import decrypt

def get_boto3_client(guild_id: int, service: str, override_region: str = None):
    config = retrieve_config(guild_id)

    if not config or "access_key" not in config:
        raise Exception("AWS 키가 설정되지 않았습니다.")
    
    access_key = decrypt(config["access_key"])
    secret_key = decrypt(config["secret_key"])
    region = override_region or config.get("region")

    if not region:
        raise Exception("리전이 설정되지 않았습니다.")
    
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

    return session.client(service)