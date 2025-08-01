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

@bot.tree.command(name="ec2status", description="EC2 상태 조회")
async def ec2status(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    config = retrieve_config(guild_id)

    if not config or not config.get("access_key"):
        await interaction.response.send_message("❌ 먼저 /setup 명령으로 키를 등록해주세요.", ephemeral=True)
        return
    
    #region 키 로그
    # print("[DEBUG] 암호문 access_key:", config["access_key"])
    # print("[DEBUG] 복호화된 access_key:", decrypt(config["access_key"]))
    # print("[DEBUG] 복호화된 secret_key:", decrypt(config["secret_key"]))
    # print("[DEBUG] region:", config["region"])
    #endregion 키 로그

    try:
        ec2 = boto3.client(
        "ec2",
        aws_access_key_id=decrypt(config["access_key"]),
        aws_secret_access_key=decrypt(config["secret_key"]),
        region_name=config["region"]
        )

        await interaction.response.defer(ephemeral=True)
        instances = get_ec2_instance_states(ec2)

        if not instances:
            msg = "🔍 실행 중인 EC2 인스턴스가 없습니다."
            #await interaction.followup.send("🔍 실행 중인 EC2 인스턴스가 없습니다.")
        else:
            msg = "\n".join([f"🖥️ {i} → `{s}`" for i, s in instances])
        await interaction.followup.send(f"{msg}",
            ephemeral=True)

    except Exception as e:
        await interaction.followup.send(f"❌ 오류 발생: {e}",
            ephemeral=True)

bot.run(TOKEN)