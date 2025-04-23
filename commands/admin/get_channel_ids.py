import discord
from discord import app_commands
from discord.ext import commands
from enum import Enum
from data.categories import CATEGORY_TO_CHANNEL

@app_commands.default_permissions(discord.Permissions(administrator=True))
@app_commands.checks.has_permissions(administrator=True)
async def get_channel_ids_command(interaction: discord.Interaction):
    forum_channels = [
        channel for channel in interaction.guild.channels
        if isinstance(channel, discord.ForumChannel)
    ]

    if not forum_channels:
        await interaction.response.send_message("❌ Tidak ada forum channel di server ini.", ephemeral=True)
        return

    hasil = "**📋 Daftar Forum Channel:**\n"
    for ch in forum_channels:
        hasil += f"- {ch.name}: `{ch.id}`\n"

    hasil += "\n\n#*Python Code:*\n"
    hasil += "=== /Topic Category ===\n"
    hasil += "class TopicCategory(Enum):\n"
    for ch in forum_channels:
        var_channel = ch.name.replace("-", "_")
        hasil += f"    {var_channel} = \"{ch.name}\"\n"
    hasil += "\nCATEGORY_TO_CHANNEL = {\n"
    for ch in forum_channels:
        var_channel = ch.name.replace("-", "_")
        hasil += f"    TopicCategory.{var_channel}.value: {ch.id},\n"
    hasil += "}\n"

    hasil += "\n=== /ask choices ===\n"
    hasil += "@app_commands.choices(category=[\n"
    for ch in forum_channels:
        if ch == forum_channels[-1]:
            hasil += f"    app_commands.Choice(name=\"{ch.name}\", value=\"{ch.name}\")\n"
        else:
            hasil += f"    app_commands.Choice(name=\"{ch.name}\", value=\"{ch.name}\"),\n"
    hasil += "])"

    await interaction.response.send_message(hasil, ephemeral=True)
