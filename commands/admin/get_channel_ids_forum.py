import discord
from discord import app_commands
from discord.ext import commands
import tempfile

@app_commands.default_permissions(discord.Permissions(administrator=True))
@app_commands.checks.has_permissions(administrator=True)
async def get_channel_ids_forum_command(interaction: discord.Interaction):
    forum_channels = [
        channel for channel in interaction.guild.channels
        if isinstance(channel, discord.ForumChannel)
    ]

    if not forum_channels:
        await interaction.response.send_message("❌ Tidak ada forum channel di server ini.", ephemeral=True)
        return

    hasil = "Daftar Forum Channel:\n"
    for ch in forum_channels:
        hasil += f"- {ch.name}: {ch.id}\n"

    # Kirim file sebagai output untuk admin
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".txt", encoding="utf-8") as temp:
        temp.write(hasil)
        temp_path = temp.name

    file = discord.File(temp_path, filename="channel_ids.txt")
    await interaction.response.send_message("📁 Berikut adalah daftar channel forum :", file=file, ephemeral=True)

