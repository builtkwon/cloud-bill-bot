import discord
from app.services.visibility_service import update_visibility

async def handle_visibility_command(interaction: discord.Interaction, is_private: bool):
    message = update_visibility(interaction.user.id, is_private)
    await interaction.response.send_message(message, ephemeral=True)
