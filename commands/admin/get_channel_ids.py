import discord
from discord import app_commands
import tempfile
import os

@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def get_channel_ids_command(interaction: discord.Interaction):
    all_channels = interaction.guild.channels

    if not all_channels:
        await interaction.response.send_message("❌ Tidak ada channel yang ditemukan di server ini.", ephemeral=True)
        return

    hasil2 = "from enum import Enum\n\n"
    hasil2 += "class Channel_Names(Enum):\n"

    filtered_channels = [ch for ch in all_channels if not isinstance(ch, (discord.CategoryChannel, discord.VoiceChannel))]

    for ch in filtered_channels:
        var_channel = ch.name.replace("-", "_").replace(" ", "_")
        hasil2 += f"    {var_channel} = \"{ch.name}\"\n"

    hasil2 += "\nChannel_Names_to_IDs = {\n"
    for ch in filtered_channels:
        var_channel = ch.name.replace("-", "_").replace(" ", "_")
        hasil2 += f"    Channel_Names.{var_channel}.value: {ch.id},\n"
    hasil2 += "}\n\n"

    hasil2 += "class Channel_IDs(Enum):\n"
    for ch in filtered_channels:
        var_channel = ch.name.replace("-", "_").replace(" ", "_")
        hasil2 += f"    {var_channel} = {ch.id}\n"

    # Tulis ke file Python secara langsung
    file_path = os.path.join("data", "all_channel_ids.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(hasil2)

    forum_channels = [
        channel for channel in interaction.guild.channels
        if isinstance(channel, discord.ForumChannel)
    ]

    if not forum_channels:
        await interaction.response.send_message("❌ Tidak ada forum channel di server ini.", ephemeral=True)
        return

    hasil = "#Python File Updated :\n" 
    hasil += file_path.replace("\\", "/") + "\n"
    
    hasil += "\n#Python File Need to be Updated Manually :\n"
    file_path_discuss = os.path.join("commands", "user", "discuss.py")
    hasil += "- " + file_path_discuss.replace("\\","/") + "\n"
    
    hasil += "\n=== /ask choices ===\n"
    hasil += "@app_commands.choices(category=[\n"
    for ch in forum_channels:
        if ch == forum_channels[-1]:
            hasil += f"    app_commands.Choice(name=\"{ch.name}\", value=\"{ch.name}\")\n"
        else:
            hasil += f"    app_commands.Choice(name=\"{ch.name}\", value=\"{ch.name}\"),\n"
    hasil += "])"

    # Kirim file sebagai output untuk admin
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".txt", encoding="utf-8") as temp:
        temp.write(hasil)
        temp_path = temp.name

    file = discord.File(temp_path, filename="channel_ids.txt")
    await interaction.response.send_message("📁 Berikut adalah daftar channel forum :", file=file, ephemeral=True)
