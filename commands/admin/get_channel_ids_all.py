import discord
from discord import app_commands
import tempfile
import os

@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def get_all_channel_ids_command(interaction: discord.Interaction):
    all_channels = interaction.guild.channels

    if not all_channels:
        await interaction.response.send_message("❌ Tidak ada channel yang ditemukan di server ini.", ephemeral=True)
        return

    hasil = "Daftar Channel (tanpa Category & Voice):\n"
    hasil2 = "from enum import Enum\n\n"
    hasil2 += "class Channel_Names(Enum):\n"

    filtered_channels = [ch for ch in all_channels if not isinstance(ch, (discord.CategoryChannel, discord.VoiceChannel))]

    for ch in filtered_channels:
        ch_type = str(ch.type).capitalize()
        hasil += f"- [{ch_type}] {ch.name}: `{ch.id}`\n"

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

    # Kirim file sebagai output untuk admin
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".txt", encoding="utf-8") as temp:
        temp.write(hasil + "\n\n#Python Code\n" + file_path.replace("\\", "/"))
        temp_path = temp.name

    file = discord.File(temp_path, filename="channel_ids.txt")
    await interaction.response.send_message("📁 Berikut adalah daftar channel (tanpa Category & Voice):", file=file, ephemeral=True)
