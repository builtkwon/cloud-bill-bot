import discord
from discord import app_commands
from infra.user_config import get_ephemeral

@app_commands.command(name="permissions", description="AWS IAM 권한 설정 방법 안내")
async def permissions_command(interaction: discord.Interaction):
    ephemeral = get_ephemeral(interaction.user.id)

    message = (
        "🔐 **AWS IAM 권한 안내**\n\n"
        "Cloud Bill Bot이 정상적으로 작동하려면 아래 권한이 필요합니다:\n\n"
        "📌 **필수 권한 목록:**\n"
        "- EC2 상태 조회: `ec2:DescribeInstances`\n"
        "- EC2 시작/중지: `ec2:StartInstances`, `ec2:StopInstances`\n"
        "- 비용 조회: `ce:GetCostAndUsage`\n"
        "- S3 조회: `s3:ListBuckets`\n"
        "- RDS 조회: `rds:DescribeDBInstances`\n"
        "- IAM 사용자 조회: `iam:ListUsers`\n\n"
        "👣 **IAM 권한 설정 방법:**\n"
        "1. [AWS 콘솔](https://console.aws.amazon.com/iam/)에 로그인\n"
        "2. 좌측 메뉴 → **사용자** → 봇 계정 선택\n"
        "3. [권한] 탭 → **권한 추가** 클릭\n"
        "4. **인라인 정책 작성** 선택 → JSON 탭 선택\n"
        "5. 아래 정책을 복사해 붙여넣고 저장:\n\n"
        "```json\n"
        "{\n"
        "  \"Version\": \"2012-10-17\",\n"
        "  \"Statement\": [\n"
        "    {\n"
        "      \"Effect\": \"Allow\",\n"
        "      \"Action\": [\n"
        "        \"ec2:DescribeInstances\",\n"
        "        \"ec2:StartInstances\",\n"
        "        \"ec2:StopInstances\",\n"
        "        \"ce:GetCostAndUsage\",\n"
        "        \"s3:ListBuckets\",\n"
        "        \"rds:DescribeDBInstances\",\n"
        "        \"iam:ListUsers\"\n"
        "      ],\n"
        "      \"Resource\": \"*\"\n"
        "    }\n"
        "  ]\n"
        "}\n"
        "```\n\n"
        "💡 정책을 저장한 뒤, 봇 명령을 다시 실행하세요."
    )

    await interaction.response.send_message(message, ephemeral=ephemeral)

@app_commands.command(name="about", description="Cloud Bill Bot 프로젝트에 대해 알아보기")
async def about_command(interaction: discord.Interaction):
    ephemeral = get_ephemeral(interaction.user.id)
    message = (
        "☁️ **Cloud Bill Bot**\n\n"
        "AWS 리소스 상태와 비용을 Discord에서 손쉽게 확인할 수 있는 봇입니다.\n"
        "개발자는 인프라 자동화와 사용성 개선을 목표로 지속적으로 기능을 확장하고 있습니다.\n\n"
        "💡 슬래시 명령어 기반으로 직관적인 UX를 지향합니다."
    )
    await interaction.response.send_message(message, ephemeral=ephemeral)

@app_commands.command(name="contact", description="개발자에게 문의하기")
async def contact_command(interaction: discord.Interaction):
    ephemeral = get_ephemeral(interaction.user.id)
    message = (
        "📬 **문의하기**\n\n"
        "궁금한 점이나 제안사항이 있다면 언제든지 디스코드로 연락주세요.\n"
        "👉 [@kwongreen](https://discord.com/users/640155697270751232)"
    )
    await interaction.response.send_message(message, ephemeral=ephemeral)
