# admin/refresh_commands.py
import discord
from discord import app_commands
from discord.ext import commands

WHITELIST_COMMANDS = ["refresh_commands"]  # Command yang tidak akan dihapus

@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def refresh_commands_command(interaction: discord.Interaction):
    try:
        await interaction.response.defer(ephemeral=True)  # ⬅️ tangguhkan dulu responsenya

        # Fetch semua command global & guild
        all_global_commands = await interaction.client.tree.fetch_commands()
        all_guild_commands = await interaction.client.tree.fetch_commands(guild=interaction.guild)

        # Hapus semua global command kecuali whitelist
        for cmd in all_global_commands:
            if cmd.name not in WHITELIST_COMMANDS:
                interaction.client.tree.remove_command(cmd.name)

        # Hapus semua guild command kecuali whitelist
        for cmd in all_guild_commands:
            if cmd.name not in WHITELIST_COMMANDS:
                interaction.client.tree.remove_command(cmd.name, guild=interaction.guild)

        # Sinkronkan ulang
        await interaction.client.tree.sync()
        await interaction.client.tree.sync(guild=interaction.guild)

        await interaction.edit_original_response(content="🔄 Semua command berhasil di-refresh (kecuali 'refresh_commands').")
    except Exception as e:
        await interaction.edit_original_response(content=f"❌ Gagal melakukan refresh command: `{e}`")
