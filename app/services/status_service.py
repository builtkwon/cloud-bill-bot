from infra.crypto import decrypt
from infra.memory_config import retrieve_config
from infra.aws_client_factory import get_boto3_session

from resources.ec2 import get_ec2_status, get_ec2_instance_states
from resources.s3 import get_s3_status
from resources.rds import get_rds_status
from resources.iam import get_iam_status

def get_resource_status_summary(guild_id: int) -> tuple[str, str]:
    config = retrieve_config(guild_id)
    if not config or not config.get("access_key"):
        return "CONFIG_ERROR", "❌ 먼저 /setup 명령으로 키를 등록해주세요."

    try:
        access_key = decrypt(config["access_key"])
        secret_key = decrypt(config["secret_key"])
        region = config["region"]

        session = get_boto3_session(access_key, secret_key, region)
        ec2 = session.client("ec2")
        s3 = session.client("s3")
        rds = session.client("rds")
        iam = session.client("iam")

        ec2_list = get_ec2_instance_states(ec2)
        ec2_active = sum(1 for inst in ec2_list if inst["State"] == "running")

        rds_instances = rds.describe_db_instances().get("DBInstances", [])
        rds_active = sum(1 for db in rds_instances if db["DBInstanceStatus"] == "available")

        # total_active = ec2_active + s3_active + rds_active + iam_active

        ec2_summary = get_ec2_status(ec2)
        s3_summary = get_s3_status(s3)
        rds_summary = get_rds_status(rds)
        iam_summary = get_iam_status(iam)

        msg = "\n".join([
             "### 📊 AWS 리소스 현황",
             "```",
             "리소스 | 실행중 | 개수",
             "------|-------|-----",
            f"EC2   | {ec2_active:<6}| {ec2_summary}",
            f"S3    | {'-':<6}| {s3_summary}",
            f"RDS   | {rds_active:<6}| {rds_summary}",
            f"IAM   | {'-':<6}| {iam_summary}",
            "```"
        ])
        return "OK", msg

    except Exception as e:
        return "ERROR", f"❌ 오류 발생: {e}"
