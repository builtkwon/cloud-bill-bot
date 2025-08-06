import discord
from app.services.region_service import get_current_region
from infra.user_config import get_ephemeral
from interface.views.region_view import RegionSelectView

async def handle_region_command(interaction: discord.Interaction):
    ephemeral = get_ephemeral(interaction.user.id)
    guild_id = interaction.guild.id
    current_region = get_current_region(guild_id)

    await interaction.response.send_message(
        content=(
            f"📍 현재 리전 : `{current_region}`\n"
            f"⚠️ `us-east-1` 리전에서만 비용 조회가 가능합니다.\n\n"
            f"아래 드롭다운에서 변경할 수 있습니다."
        ),
        view=RegionSelectView(guild_id),
        ephemeral=ephemeral
    )
