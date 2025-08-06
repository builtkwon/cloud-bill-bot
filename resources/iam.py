def get_iam_status(client):
    try:
        users = client.list_users().get("Users",[])
        return f"{len(users)}명"
    except Exception as e:
        return f"[ERROR] {e}"