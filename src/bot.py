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

@bot.tree.command(name="account", description="현재 사용중인 AWS 계정 ID 조회")
async def account(interaction:discord.Interaction):
    guild_id = interaction.guild.id
    config = retrieve_config(guild_id)
    
    account_id = config.get("account_id")
    user_name = config.get("user_name","")

    if not account_id:
        await interaction.response.send_message("❌ 아직 AWS 계정이 등록되지 않았습니다. `/setup`을 진행해 주세요.",ephemeral=True)
        return
    
    msg_lines = [f"✅ 현재 등록된 AWS 계정 ID : `{account_id}`"]
    if user_name:
        msg_lines.append(f"✅ IAM 사용자 이름 : `{user_name}`")
        
    await interaction.response.send_message("\n".join(msg_lines), ephemeral=True)

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
            ec2_summary = f"[ERROR] {e}"

        try: 
            s3_buckets = s3.list_buckets().get("Buckets", [])
            s3_summary = f"{len(s3_buckets)}개"
        except Exception as e:
            s3_summary = f"[ERROR] {e}"

        try:
            rds_instances = rds.describe_db_instances().get("DBInstances",[])
            rds_summary = (
                f"{len(rds_instances)}개"
                if rds_instances else "0개"
            )
        except Exception as e:
            rds_summary = f"[ERROR] {e}"

        try:
            iam_users = iam.list_users().get("Users",[])
            iam_summary = f"{len(iam_users)}명"
        except Exception as e:
            iam_summary = f"[ERROR] {e}"

        msg = "\n".join([
            "### 📊 AWS 리소스 요약",
            "```",
            "리소스 | 상태",
            "------|-------",
            f"EC2   | {ec2_summary}",
            f"S3    | {s3_summary}",
            f"RDS   | {rds_summary}",
            f"IAM   | {iam_summary}",
            "```"
        ])

        await interaction.followup.send(msg)

    except Exception as e:
        await interaction.followup.send(f"❌ 오류 발생: {e}")

bot.run(TOKEN)