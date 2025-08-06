import discord
from discord import app_commands
from app.commands.status_handler import handle_status_command

@app_commands.command(name="status", description="전체 리소스 상태 조회")
async def status_command(interaction: discord.Interaction):
    await handle_status_command(interaction)
