import boto3
from infra.crypto import decrypt
from infra.memory_config import retrieve_config

def get_boto3_session(access_key: str, secret_key: str, region: str) -> boto3.Session:
    return boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

def get_boto3_client(guild_id: int, service_name: str, override_region: str = None):
    config = retrieve_config(guild_id)

    access_key = decrypt(config["access_key"])
    secret_key = decrypt(config["secret_key"])
    region = override_region or config["region"]

    session = get_boto3_session(access_key, secret_key, region)
    return session.client(service_name)
