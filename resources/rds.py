def get_rds_status(client):
    try:
        instances = client.describe_db_instances().get("DBInstances", [])
        return f"{len(instances)}개" if instances else "0개"
    except Exception as e:
        return f"[ERROR] {e}"