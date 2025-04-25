import discord
from discord import app_commands
import os
from utils.bot.bot_setup import bot
ANNOUNCEMENT_CHANNEL_ID = 1364799478204207157

@app_commands.default_permissions(discord.Permissions(administrator=True))
@app_commands.checks.has_permissions(administrator=True)
async def shutdown_bot_command(interaction: discord.Interaction):
    await interaction.response.send_message("🔄 Command shutdown dieksekusi", ephemeral=True)
    announcement_channel = bot.get_channel(ANNOUNCEMENT_CHANNEL_ID)
    if announcement_channel:
        await announcement_channel.send("🔄 Bot dimatikan...")
    await interaction.client.close()
