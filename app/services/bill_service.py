from datetime import date
from infra.crypto import decrypt
from infra.memory_config import retrieve_config
from infra.aws_client_factory import get_boto3_client
import FinanceDataReader as fdr

def get_billing_summary(guild_id: int) -> tuple[str, str]:
    config = retrieve_config(guild_id)
    if not config or not config.get("access_key"):
        return "CONFIG_ERROR", "❌ 먼저 /setup 명령으로 키를 등록해주세요."

    region = config.get("region", "us-east-1")
    if region != "us-east-1":
        return "UNSUPPORTED_REGION", (
            f"❌ 현재 선택된 리전 `{region}`은 Cost Explorer를 지원하지 않습니다.\n"
            f"`us-east-1` 리전에서만 비용 조회가 가능합니다."
        )

    try:
        ce = get_boto3_client(guild_id, "ce", override_region="us-east-1")
        today = date.today()
        start = today.replace(day=1).isoformat()
        end = today.isoformat()

        response = ce.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"]
        )

        amount = response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
        currency = response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Unit"]

        msg = f"💰 이번 달 누적 청구 금액 : \n`{float(amount):,.2f} {currency}`"

        rate_info = ""
        if currency == "USD":
            try:
                rate = fdr.DataReader("USD/KRW").iloc[-1].iloc[0]
                krw = float(amount) * rate
                rate_info = f"\n 한화 : `{krw:.0f}원` \n환율 :`(1 USD ≈ {rate:,.2f} KRW)`"
            except Exception as ex:
                rate_info = f"\n [ERROR] 환율 정보를 불러올 수 없습니다 \n {ex}"

        return "OK", f"💰\n청구 금액 : `{float(amount):,.2f}{currency}`{rate_info}"

    except Exception as e:
        return "ERROR", f"[ERROR] : {e}"
