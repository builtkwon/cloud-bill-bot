import discord
from discord import app_commands
from app.commands.region_handler import handle_region_command

@app_commands.command(name="region", description="현재 설정된 리전 조회 및 업데이트")
async def region_command(interaction: discord.Interaction):
    await handle_region_command(interaction)
