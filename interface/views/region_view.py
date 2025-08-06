import discord
from infra.memory_config import retrieve_config, store_config

REGION_OPTIONS = [
    discord.SelectOption(label="버지니아 북부 / us-east-1", value="us-east-1"),
    discord.SelectOption(label="오하이오 / us-east-2", value="us-east-2"),
    discord.SelectOption(label="캘리포니아 / us-west-1", value="us-west-1"),
    discord.SelectOption(label="오레곤 / us-west-2", value="us-west-2"),
    discord.SelectOption(label="도쿄 / ap-northeast-1", value="ap-northeast-1"),
    discord.SelectOption(label="서울 / ap-northeast-2", value="ap-northeast-2"),
    discord.SelectOption(label="오사카 / ap-northeast-3", value="ap-northeast-3"),
    discord.SelectOption(label="싱가포르 / ap-southeast-1", value="ap-southeast-1"),
    discord.SelectOption(label="시드니 / ap-southeast-2", value="ap-southeast-2"),
]

class RegionSelect(discord.ui.Select):
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        super().__init__(
            placeholder="AWS 리전을 선택하세요",
            options=REGION_OPTIONS,
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        config = retrieve_config(self.guild_id)
        config["region"] = self.values[0]
        store_config(self.guild_id, config)

        await interaction.response.send_message(
            f"✅ 리전 변경됨 : `{self.values[0]}`",
            ephemeral=True
        )

class RegionSelectView(discord.ui.View):
    def __init__(self, guild_id: int):
        super().__init__(timeout=60)
        self.add_item(RegionSelect(guild_id))
