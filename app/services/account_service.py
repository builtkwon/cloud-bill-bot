from infra.memory_config import retrieve_config

def get_account_info(guild_id: int) -> tuple[bool, str]:
    config = retrieve_config(guild_id)
    if not config:
        return False, "❌ 아직 AWS 계정이 등록되지 않았습니다. `/setup`을 진행해 주세요."

    account_id = config.get("account_id")
    user_name = config.get("user_name", "")

    if not account_id:
        return False, "❌ 아직 AWS 계정이 등록되지 않았습니다. `/setup`을 진행해 주세요."

    msg_lines = [f"✅ 현재 등록된 AWS 계정 ID : `{account_id}`"]
    if user_name:
        msg_lines.append(f"✅ IAM 사용자 이름 : `{user_name}`")

    return True, "\n".join(msg_lines)
