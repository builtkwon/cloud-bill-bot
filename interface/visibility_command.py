import discord
from discord import app_commands
from app.commands.visibility_handler import handle_visibility_command

@app_commands.command(name="public", description="명령어 응답을 전체공개로 설정합니다.")
async def public_command(interaction: discord.Interaction):
    await handle_visibility_command(interaction, is_private=False)

@app_commands.command(name="private", description="명령어 응답을 나만 보기로 설정합니다.")
async def private_command(interaction: discord.Interaction):
    await handle_visibility_command(interaction, is_private=True)
