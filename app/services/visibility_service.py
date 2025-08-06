from infra.user_config import set_ephemeral

def update_visibility(user_id: int, is_private: bool) -> str:
    set_ephemeral(user_id, is_private)
    return (
        "✅ 이후 모든 응답은 **나만보기**로 표시됩니다."
        if is_private else
        "✅ 이후 모든 응답은 **전체공개**로 표시됩니다."
    )
