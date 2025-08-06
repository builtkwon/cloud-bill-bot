import discord
from discord.ui import View, Select, Button
from infra.memory_config import retrieve_config
from infra.aws_client_factory import get_boto3_client
from resources.ec2 import start_instance, stop_instance, get_ec2_instances_with_names

class EC2Select(Select):
    def __init__(self, options, parent_view):
        super().__init__(
            placeholder="제어할 EC2 인스턴스를 선택하세요",
            options=options,
            min_values=1,
            max_values=1
        )
        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        self.parent_view.selected_instance_id = self.values[0]
        await interaction.response.send_message(f"✅ 선택됨: `{self.values[0]}`", ephemeral=True)

class EC2ControlView(View):
    def __init__(self, guild_id: int):
        super().__init__(timeout=60)
        self.guild_id = guild_id
        self.selected_instance_id = None

        # 인스턴스 목록 조회
        client = get_boto3_client(guild_id, "ec2")
        instances = get_ec2_instances_with_names(client)

        options = [
            discord.SelectOption(
                label=f"{name} ({state})",
                value=instance_id
            )
            for instance_id, name, state in instances
        ]

        self.select_menu = EC2Select(options, self)
        self.add_item(self.select_menu)
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return True

    @discord.ui.button(label="Start", style=discord.ButtonStyle.success)
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.selected_instance_id:
            await interaction.response.send_message("❌ 먼저 인스턴스를 선택해주세요.", ephemeral=True)
            return

        client = get_boto3_client(self.guild_id, "ec2")
        result = start_instance(client, self.selected_instance_id)

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(content=result, view=self)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger, custom_id="stop")
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.selected_instance_id:
            await interaction.response.send_message("❌ 먼저 인스턴스를 선택해주세요.", ephemeral=True)
            return

        client = get_boto3_client(self.guild_id, "ec2")
        result = stop_instance(client, self.selected_instance_id)

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(content=result, view=self)
