import discord
from discord import app_commands
from app.commands.bill_handler import handle_bill_command

@app_commands.command(name="bill", description="전체 비용 청구 상태 조회")
async def bill_command(interaction: discord.Interaction):
    await handle_bill_command(interaction)
