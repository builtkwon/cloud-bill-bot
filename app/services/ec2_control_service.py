from infra.aws_client_factory import get_boto3_client
from resources.ec2 import get_ec2_instances_with_names, start_instance, stop_instance


def get_ec2_instance_options(guild_id: int) -> list[tuple[str, str, str]]:
    """
    EC2 인스턴스 목록을 (InstanceId, Name, State) 형태로 반환
    """
    try:
        client = get_boto3_client(guild_id, "ec2")
        return get_ec2_instances_with_names(client)
    except Exception as e:
        return [("ERROR", str(e), "")]


def start_ec2_instance(guild_id: int, instance_id: str) -> str:
    try:
        client = get_boto3_client(guild_id, "ec2")
        return start_instance(client, instance_id)
    except Exception as e:
        return f"❌ 시작 실패: {str(e)}"


def stop_ec2_instance(guild_id: int, instance_id: str) -> str:
    try:
        client = get_boto3_client(guild_id, "ec2")
        return stop_instance(client, instance_id)
    except Exception as e:
        return f"❌ 중지 실패: {str(e)}"
