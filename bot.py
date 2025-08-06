import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from pathlib import Path

from interface.setup_command import setup_command
from interface.region_command import region_command
from interface.account_command import account_command
from interface.status_command import status_command
from interface.bill_command import bill_command
from interface.visibility_command import public_command, private_command
from interface.ec2_control_command import ec2control_command
from interface.text_command import permissions_command, about_command, contact_command

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    bot.tree.add_command(setup_command)
    bot.tree.add_command(region_command)
    bot.tree.add_command(account_command)
    bot.tree.add_command(status_command)
    bot.tree.add_command(bill_command)
    bot.tree.add_command(public_command)
    bot.tree.add_command(private_command)
    bot.tree.add_command(ec2control_command)
    bot.tree.add_command(permissions_command)
    bot.tree.add_command(about_command)
    bot.tree.add_command(contact_command)

    synced = await bot.tree.sync()
    print(f"✅ 봇 로그인: {bot.user}")
    print(f"🌐 글로벌 명령어 {len(synced)}개 동기화 완료")

@bot.event
async def on_guild_join(guild):
    await bot.tree.sync(guild=guild)
    print(f"🆕 신규 서버: {guild.name} 동기화 완료")

bot.run(TOKEN)