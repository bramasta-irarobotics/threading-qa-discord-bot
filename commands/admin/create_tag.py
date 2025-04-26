import discord
from discord import app_commands
from data.all_channel_ids import Channel_IDs

# Ambil channel ID dari channel forum
forum_channel_id = Channel_IDs.discussion_threads.value  # Ganti sesuai channel ID yang kamu mau

@app_commands.default_permissions(discord.Permissions(administrator=True))
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(name="Nama tag yang akan dibuat") 
async def create_tag_command(interaction: discord.Interaction, name: str):
    if forum_channel_id is None:
        await interaction.response.send_message("❌ ID forum untuk kategori 'General' tidak ditemukan.", ephemeral=True)
        return

    forum_channel = interaction.guild.get_channel(forum_channel_id)

    if not isinstance(forum_channel, discord.ForumChannel):
        await interaction.response.send_message("❌ Channel yang ditentukan bukan forum channel.", ephemeral=True)
        return

    try:
        await forum_channel.create_tag(name=name)
        await interaction.response.send_message(f"✅ Tag `{name}` berhasil dibuat di {forum_channel.mention}.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"❌ Gagal membuat tag: {e}", ephemeral=True)
