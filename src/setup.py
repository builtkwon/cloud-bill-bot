import discord
import boto3
from discord import app_commands
from discord.ui import Modal, TextInput, View, Select
from utils.crypto import encrypt, decrypt
from utils.memory_config import store_config, retrieve_config
from region_view import SetupView
from datetime import date

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

        try:
            session = boto3.Session(
                aws_access_key_id=access,
                aws_secret_access_key=secret
            )
            sts = session.client("sts")
            identity = sts.get_caller_identity()
            account_id = identity["Account"]
            arn = identity["Arn"]
            user_name = arn.split("/")[-1] if ":user/" in arn else ""
        except Exception as e:
            await interaction.response.send_message(
                f"❌ AWS 계정 인증 실패: {e}", ephemeral=True
            )
            return

        store_config(guild_id, {
            "access_key": encrypt(access),
            "secret_key": encrypt(secret),
            "region": None,
            "account_id": account_id,
            "user_name": user_name
        })

        await interaction.response.send_message(
            "✅ 키 저장 완료! 리전을 선택해주세요.",
            view=SetupView(guild_id),
            ephemeral=True
        )


@app_commands.command(name="setup", description="AWS 키와 리전을 설정합니다.")
async def setup(interaction: discord.Interaction):
    await interaction.response.send_modal(AWSKeyModal(interaction))