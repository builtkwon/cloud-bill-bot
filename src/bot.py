import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
import boto3
import discord
from discord.ext import commands
from dotenv import load_dotenv

from aws_handler import get_ec2_instance_states
from setup import setup
from utils.memory_config import retrieve_config
from utils.crypto import decrypt

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    bot.tree.add_command(setup)
    synced = await bot.tree.sync()
    print(f"✅ 봇 로그인: {bot.user}")
    print(f"🌐 글로벌 명령어 {len(synced)}개 동기화 완료")

@bot.event
async def on_guild_join(guild):
    await bot.tree.sync(guild=guild)
    print(f"🆕 신규 서버: {guild.name} 동기화 완료")

# @bot.tree.command(name="ec2status", description="EC2 상태 조회")
# async def ec2status(interaction: discord.Interaction):
#     guild_id = interaction.guild.id
#     config = retrieve_config(guild_id)

#     if not config or not config.get("access_key"):
#         await interaction.response.send_message("❌ 먼저 /setup 명령으로 키를 등록해주세요.", ephemeral=True)
#         return
    
#     #region 키 로그
#     # print("[DEBUG] 암호문 access_key:", config["access_key"])
#     # print("[DEBUG] 복호화된 access_key:", decrypt(config["access_key"]))
#     # print("[DEBUG] 복호화된 secret_key:", decrypt(config["secret_key"]))
#     # print("[DEBUG] region:", config["region"])
#     #endregion 키 로그

#     try:
#         ec2 = boto3.client(
#         "ec2",
#         aws_access_key_id=decrypt(config["access_key"]),
#         aws_secret_access_key=decrypt(config["secret_key"]),
#         region_name=config["region"]
#         )

#         await interaction.response.defer(ephemeral=True)
#         instances = get_ec2_instance_states(ec2)

#         if not instances:
#             msg = "🔍 실행 중인 EC2 인스턴스가 없습니다."
#             #await interaction.followup.send("🔍 실행 중인 EC2 인스턴스가 없습니다.")
#         else:
#             msg = "\n".join([f"🖥️ {i} → `{s}`" for i, s in instances])
#         await interaction.followup.send(f"{msg}",
#             ephemeral=True)

#     except Exception as e:
#         await interaction.followup.send(f"❌ 오류 발생: {e}",
#             ephemeral=True)

# 동작 확인해야함
@bot.tree.command(name="account", description="현재 사용중인 AWS 계정 ID")
async def account(interaction:discord.Interaction):
    try:
        account_id = boto3.client('sts').get_caller_identity().get('Account')
        now_acc = (f"> 현재 연결된 계정 : {account_id}")
    except Exception:
        now_acc = "❌ 현재 연결된 AWS 계정이 없습니다."
    await interaction.response.send_message(now_acc, ephemeral=True)

@bot.tree.command(name="status", description="전체 리소스 상태 조회")
async def status(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    config = retrieve_config(guild_id)

    if not config or not config.get("access_key"):
        await interaction.response.send_message("❌ 먼저 /setup 명령으로 키를 등록해주세요.", ephemeral=True)
        return
    
    try:
        await interaction.response.defer(ephemeral=True)

        access_key = decrypt(config["access_key"])
        secret_key = decrypt(config["secret_key"])
        region = config["region"]

        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        ec2 = session.client("ec2")
        s3 = session.client("s3")
        rds = session.client("rds")
        iam = session.client("iam")
        
        try :
            ec2_instances = get_ec2_instance_states(ec2)
            ec2_summary = (
                f"{len(ec2_instances)}개"
                if ec2_instances else "0개"
            )
        except Exception as e:
            ec2_summary = f" EC2 오류    : {e}"

        try: 
            s3_buckets = s3.list_buckets().get("Buckets", [])
            s3_summary = f" S3 버킷      : {len(s3_buckets)}개"
        except Exception as e:
            s3_summary = f" S3 오류      : {e}"

        try:
            rds_instances = rds.describe_db_instances().get("DBInstances",[])
            rds_summary = (
                f" RDS 인스턴스 : {len(rds_instances)}개"
                if rds_instances else " RDS 인스턴스 : 0개"
            )
        except Exception as e:
            rds_summary = f" RDS 오류     : {e}"

        try:
            iam_users = iam.list_users().get("Users",[])
            iam_summary = f" IAM 사용자   : {len(iam_users)}명"
        except Exception as e:
            iam_summary = f" IAM 오류     : {e}"

        msg = "\n".join([
            " **AWS 리소스 요약**",
            ec2_summary,
            s3_summary,
            rds_summary,
            iam_summary
        ])
        # msg - "\n",join({
        #     "### 📊 AWS 리소스 요약",
        #     "```",
        #     "리소스 | 상태",
        #     "------|-------",
        #     "EC2   | {ec2_summary}",
        #     "S3",
        #     "RDS",
        #     "IAM",
        #     "```"
        # })

        await interaction.followup.send(msg)

    except Exception as e:
        await interaction.followup.send(f"❌ 오류 발생: {e}")

bot.run(TOKEN)