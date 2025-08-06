import discord
from interface.views.ec2_control_view import EC2ControlView
from app.services.ec2_control_service import get_ec2_instance_options

async def handle_ec2_control_command(interaction: discord.Interaction):
    guild_id = interaction.guild.id

    try:
        await interaction.response.defer(ephemeral=True)
        
        instances = get_ec2_instance_options(guild_id)
        if not instances or instances[0][0] == "ERROR":
            await interaction.followup.send(
                "🚫 실행 가능한 EC2 인스턴스를 찾을 수 없습니다."
            )
            return

        view = EC2ControlView(guild_id)
        await interaction.followup.send(
            content="제어할 EC2 인스턴스를 선택하세요:",
            view=view
        )

    except Exception as e:
        await interaction.followup.send(
            content=f"❌ 오류 발생: {e}"
        )
