import discord
from infra.user_config import get_ephemeral
from infra.memory_config import retrieve_config
from app.services.status_service import get_resource_status_summary

async def handle_status_command(interaction: discord.Interaction):
    ephemeral = get_ephemeral(interaction.user.id)
    guild_id = interaction.guild.id

    config = retrieve_config(guild_id)
    if not config or not config.get("access_key"):
        await interaction.response.send_message(
            "❌ 먼저 /setup 명령으로 키를 등록해주세요.",
            ephemeral=ephemeral
        )
        return

    await interaction.response.defer(ephemeral=ephemeral)

    status, result = get_resource_status_summary(guild_id)

    await interaction.followup.send(result)
