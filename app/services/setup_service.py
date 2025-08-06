import boto3
from infra.crypto import encrypt
from infra.memory_config import store_config

def validate_and_store_aws_keys(guild_id: int, access: str, secret: str) -> tuple[bool, str, str]:
    try:
        session = boto3.Session(
            aws_access_key_id=access,
            aws_secret_access_key=secret
        )
        sts = session.client("sts")
        identity = sts.get_caller_identity()
        account_id = identity["Account"]
        arn = identity["Arn"]
        user_name = arn.split("/")[-1] if ":user/" in arn else ""
    except Exception as e:
        return False, f"❌ AWS 계정 인증 실패: {e}", ""

    store_config(guild_id, {
        "access_key": encrypt(access),
        "secret_key": encrypt(secret),
        "region": None,
        "account_id": account_id,
        "user_name": user_name
    })

    return True, (
    "✅ 키 저장 완료! 리전을 선택해주세요.\n\n"
    "⚠️ **권한 안내 : /permissions 입력**"
), account_id
