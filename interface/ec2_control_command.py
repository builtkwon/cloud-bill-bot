import discord
from discord import app_commands
from app.commands.ec2_control_handler import handle_ec2_control_command

@app_commands.command(name="ec2control", description="EC2 인스턴스를 선택하고 제어합니다")
async def ec2control_command(interaction: discord.Interaction):
    await handle_ec2_control_command(interaction)
