import discord
from discord.ui import Modal, TextInput
from app.services.setup_service import validate_and_store_aws_keys
from interface.views.region_view import RegionSelectView  # ✅ 공통 View만 사용

class AWSKeyModal(Modal, title="AWS 키 입력"):
    access_key = TextInput(label="Access Key", placeholder="enter your key", required=True)
    secret_key = TextInput(label="Secret Key", placeholder="enter your secret key", required=True, style=discord.TextStyle.paragraph)

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        access = self.access_key.value.strip()
        secret = self.secret_key.value.strip()

        success, message, _ = validate_and_store_aws_keys(guild_id, access, secret)

        await interaction.response.send_message(
            content=message,
            view=RegionSelectView(guild_id),
            ephemeral=True
        )

async def handle_setup_command(interaction: discord.Interaction):
    await interaction.response.send_modal(AWSKeyModal(interaction))
