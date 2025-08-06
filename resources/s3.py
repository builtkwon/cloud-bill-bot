def get_s3_status(client):
    try:
        buckets = client.list_buckets().get("Buckets", [])
        return f"{len(buckets)}개"
    except Exception as e:
        return f"[ERROR] {e}"