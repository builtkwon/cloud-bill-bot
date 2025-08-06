from botocore.exceptions import ClientError

def get_ec2_status(client):
    try:
        instances = get_ec2_instance_states(client)
        return f"{len(instances)}개" if instances else "0개"
    except Exception as e:
        return f"[ERROR] {e}"

def get_ec2_instances_with_names(client):
    result = []
    try:
        response = client.describe_instances()
        for r in response["Reservations"]:
            for i in r["Instances"]:
                instance_id = i["InstanceId"]
                state = i["State"]["Name"]
                name = next((t["Value"]for t in i.get("Tags",[]) if t["Key"] == "Name"), "N/A")
                result.append((instance_id, name, state))
    except Exception as e:
        result = [("[ERROR]",str(e),"")]
    return result

def start_instance(client, instance_id: str):
    try:
        response = client.start_instances(InstanceIds=[instance_id])
        return f"✅ 인스턴스 시작 요청됨: `{instance_id}`"
    except ClientError as e:
        return f"❌ 중지 실패: {e.response['Error']['Message']}"
    except Exception as e:
        return f"❌ 예외 발생: {str(e)}"

def stop_instance(client, instance_id: str):
    try:
        response = client.stop_instances(InstanceIds=[instance_id])
        return f"🛑 인스턴스 중지 요청됨: `{instance_id}`"
    except ClientError as e:
        return f"❌ 중지 실패: {e.response['Error']['Message']}"
    except Exception as e:
        return f"❌ 예외 발생: {str(e)}"

def get_ec2_instance_states(client) -> list:
    instances = []

    try:
        response = client.describe_instances()
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instances.append({
                    "InstanceId": instance["InstanceId"],
                    "State": instance["State"]["Name"],
                    "Type": instance["InstanceType"],
                    "Name": next(
                        (tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Name"),
                        "Unnamed"
                    )
                })
        return instances
    except Exception as e:
        return [{"InstanceId": "ERROR", "State": str(e), "Type": "-", "Name": "-"}]
