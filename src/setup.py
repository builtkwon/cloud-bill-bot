import discord
from discord import app_commands
from discord.ui import Modal, TextInput, View, Select
from utils.crypto import encrypt
from utils.memory_config import store_config
from region_view import SetupView

class AWSKeyModal(Modal, title="AWS 키 입력"):
    access_key = TextInput(label="Access Key", placeholder="AKIA...", required=True)
    secret_key = TextInput(label="Secret Key", placeholder="********", required=True, style=discord.TextStyle.paragraph)

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id

        access = self.access_key.value.strip()
        secret = self.secret_key.value.strip()

        store_config(guild_id, {
            "access_key": encrypt(access),
            "secret_key": encrypt(secret),
            "region": None
        })

        await interaction.response.send_message(
            "✅ 키 저장 완료! 리전을 선택해주세요.",
            view=SetupView(guild_id),
            ephemeral=True
        )

@app_commands.command(name="setup", description="AWS 키와 리전을 설정합니다.")
async def setup(interaction: discord.Interaction):
    await interaction.response.send_modal(AWSKeyModal(interaction))