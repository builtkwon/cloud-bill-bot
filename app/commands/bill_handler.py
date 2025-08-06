import discord
from app.services.bill_service import get_billing_summary
from infra.user_config import get_ephemeral

async def handle_bill_command(interaction: discord.Interaction):
    ephemeral = get_ephemeral(interaction.user.id)
    guild_id = interaction.guild.id

    status, result = get_billing_summary(guild_id)

    if status in ("CONFIG_ERROR", "UNSUPPORTED_REGION"):
        await interaction.response.send_message(result, ephemeral=ephemeral)
    else:
        await interaction.response.defer(ephemeral=ephemeral)
        await interaction.followup.send(result)
