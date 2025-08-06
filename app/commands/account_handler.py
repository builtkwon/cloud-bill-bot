import discord
from app.services.account_service import get_account_info
from infra.user_config import get_ephemeral

async def handle_account_command(interaction: discord.Interaction):
    ephemeral = get_ephemeral(interaction.user.id)
    guild_id = interaction.guild.id

    ok, message = get_account_info(guild_id)
    await interaction.response.send_message(message, ephemeral=ephemeral)
