from infra.crypto import decrypt
from infra.memory_config import retrieve_config
from infra.aws_client_factory import get_boto3_session

from resources.ec2 import get_ec2_status
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

        ec2_summary = get_ec2_status(ec2)
        s3_summary = get_s3_status(s3)
        rds_summary = get_rds_status(rds)
        iam_summary = get_iam_status(iam)

        msg = "\n".join([
            "### 📊 AWS 리소스 요약",
            "```",
            "리소스 | 상태",
            "------|-------",
            f"EC2   | {ec2_summary}",
            f"S3    | {s3_summary}",
            f"RDS   | {rds_summary}",
            f"IAM   | {iam_summary}",
            "```"
        ])
        return "OK", msg

    except Exception as e:
        return "ERROR", f"❌ 오류 발생: {e}"
