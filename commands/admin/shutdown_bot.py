import discord
from discord import app_commands
import os
ANNOUNCEMENT_CHANNEL_ID = 1365172459669557305

@app_commands.default_permissions(discord.Permissions(administrator=True))
@app_commands.checks.has_permissions(administrator=True)
async def shutdown_bot_command(interaction: discord.Interaction):
    await interaction.response.send_message("🔄 Command shutdown dieksekusi", ephemeral=True)
    announcement_channel = interaction.client.get_channel(ANNOUNCEMENT_CHANNEL_ID)
    if announcement_channel:
        await announcement_channel.send("🔄 Bot dimatikan...")
    await interaction.client.close()
