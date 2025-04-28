import discord
from discord import app_commands
import os
ANNOUNCEMENT_CHANNEL_ID = 1365172459669557305

@app_commands.default_permissions(discord.Permissions(administrator=True))
@app_commands.checks.has_permissions(administrator=True)
async def restart_bot_command(interaction: discord.Interaction):
    await interaction.response.send_message("🔄 Command restart dieksekusi", ephemeral=True)
    announcement_channel = interaction.client.get_channel(ANNOUNCEMENT_CHANNEL_ID)
    if announcement_channel:
        await announcement_channel.send("🔄 Bot sedang restart...")
    await interaction.client.close()

    python_exe = r"D:/Testing-Bot-TestOnly/threading-qa-discord-bot/env/Scripts/python.exe"
    main_script = r"D:/Testing-Bot-TestOnly/threading-qa-discord-bot/main.py"

    os.execv(python_exe, [python_exe, main_script])
