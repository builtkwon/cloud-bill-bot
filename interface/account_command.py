import discord
from discord import app_commands
from app.commands.account_handler import handle_account_command

@app_commands.command(name="account", description="현재 사용중인 AWS 계정 ID 조회")
async def account_command(interaction: discord.Interaction):
    await handle_account_command(interaction)
