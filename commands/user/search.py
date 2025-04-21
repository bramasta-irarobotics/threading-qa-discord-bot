import discord
from discord import app_commands
from discord.ext import commands
from utils.bot.bot_setup import bot
from data.categories import CATEGORY_TO_CHANNEL

@app_commands.describe(keyword="Keyword yang ingin dicari")
async def search_command(interaction: discord.Interaction, keyword: str):
    await interaction.response.defer(ephemeral=True, thinking=True)

    results = []
    for forum_id in CATEGORY_TO_CHANNEL.values():
        forum = bot.get_channel(forum_id)
        if not isinstance(forum, discord.ForumChannel):
            continue
        for thread in forum.threads:
            if keyword.lower() in thread.name.lower():
                results.append(thread)

    if not results:
        await interaction.followup.send(f"❌ Tidak ditemukan pertanyaan dengan keyword: `{keyword}`", ephemeral=True)
        return

    hasil = f"🔍 **Hasil pencarian untuk:** `{keyword}`\n"
    for t in results[:10]:
        hasil += f"- [{t.name}]({t.jump_url})\n"

    await interaction.followup.send(hasil, ephemeral=True)
