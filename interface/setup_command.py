import discord
from discord import app_commands
from app.commands.setup_handler import handle_setup_command

@app_commands.command(name="setup", description="AWS 키와 리전을 설정합니다.")
async def setup_command(interaction: discord.Interaction):
    await handle_setup_command(interaction)
