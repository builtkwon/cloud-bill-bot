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

#region PastViewCode
# import discord
# from discord import app_commands
# from utils.crypto import encrypt
# from utils.memory_config import store_config, retrieve_config

# TEMP_AWS_DATA = {}

# # 리전 드롭다운 여기다 지은아
# class SetupView(discord.ui.View):
#     def __init__(self, guild_id):
#         super().__init__(timeout=60)
#         self.guild_id = guild_id
#         self.select = discord.ui.Select(
#             placeholder="AWS 계정 리전을 선택하세요",
#             options=[
#                 discord.SelectOption(label="버지니아 북부/us-east-1", value="us-east-1"),
#                 discord.SelectOption(label="오하이오/us-east-2", value="us-east-2"),
#                 discord.SelectOption(label="캘리포니아/us-west-1", value="us-west-1"),
#                 discord.SelectOption(label="오래곤/us-west-2", value="us-west-2"),
#                 discord.SelectOption(label="도쿄/ap-northeast-1", value="ap-northeast-1"),
#                 discord.SelectOption(label="서울/ap-northeast-2", value="ap-northeast-2"),
#                 discord.SelectOption(label="오사카/ap-northeast-3", value="ap-northeast-3"),
#                 discord.SelectOption(label="싱가포르/ap-southeast-1", value="ap-southeast-1"),
#                 discord.SelectOption(label="시드니/ap-southeast-2", value="ap-southeast-2")
#             ]
#         )
#         self.select.callback = self.region_selected
#         self.add_item(self.select)
    
#     async def region_selected(self, interaction: discord.Interaction):
#         config = retrieve_config(self.guild_id)
#         if not config:
#             await interaction.response.send_message("❌ AWS 키 정보를 먼저 등록해주세요.", ephemeral=True)
#             return
        
#         config["region"] = self.select.values[0]
#         store_config(self.guild_id, config)
#         await interaction.response.send_message(f"✅ 리전 설정 완료: `{config['region']}`", ephemeral=True)
    
# # /setup 명령 여기부터
# @app_commands.command(name="setup", description="AWS 연동을 위한 키와 리전을 설정합니다.\n 직접 AWS에서 확인한 값을 정확히 입력해 주세요.")
# async def setup(interaction: discord.Interaction):
#     guild_id = interaction.guild.id
#     await interaction.response.send_message("🔐 AWS Access Key를 입력해주세요:", ephemeral=True)

#     def check(m):
#         return m.author.id == interaction.user.id and m.channel == interaction.channel

#     try:
#         access_msg = await interaction.client.wait_for("message", check=check, timeout=60)
#         access_key = encrypt(access_msg.content)

#         await interaction.followup.send("🔐 AWS Secret Key를 입력해주세요:", ephemeral=True)
#         secret_msg = await interaction.client.wait_for("message", check=check, timeout=60)
#         secret_key = encrypt(secret_msg.content)

#         store_config(guild_id, {
#             "access_key": access_key,
#             "secret_key": secret_key,
#             "region":None
#         })

#         await interaction.followup.send(
#             "🌍 리전을 선택해주세요:", 
#             view=SetupView(guild_id), 
#             ephemeral=True
#         )
#         print("[DEBUG][SETUP] 입력된 access_key 평문:", access_msg.content.strip())
#         print("[DEBUG][SETUP] 입력된 secret_key 평문:", secret_msg.content.strip())
    

#     except Exception as e:
#         await interaction.followup.send(f"❌ 오류 발생: {e}", ephemeral=True)
#endregion PastViewCode