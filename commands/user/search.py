import discord
from discord import app_commands
from discord.ext import commands
from data.all_channel_ids import Channel_IDs
forum_id = Channel_IDs.discussion_threads.value

# Fungsi autocomplete tag
async def autocomplete_tags(
    interaction: discord.Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    forum_channel = interaction.client.get_channel(forum_id)

    if not isinstance(forum_channel, discord.ForumChannel):
        return []

    return [
        app_commands.Choice(name=tag.name, value=tag.name)
        for tag in forum_channel.available_tags
        if current.lower() in tag.name.lower()
    ][:25]  # Max 25 pilihan sesuai limit Discord
# Slash command utama
@app_commands.describe(
    keyword="Keyword yang ingin dicari",
    tag1="Tag pertama (opsional)",
    tag2="Tag kedua (opsional)",
    tag3="Tag ketiga (opsional)"
)
@app_commands.autocomplete(tag1=autocomplete_tags, tag2=autocomplete_tags, tag3=autocomplete_tags)
async def search_command(
    interaction: discord.Interaction, 
    keyword: str,
    tag1: str = None,
    tag2: str = None,
    tag3: str = None):
    
    await interaction.response.defer(ephemeral=True, thinking=True)

    results = []
    forum = interaction.client.get_channel(forum_id)
    
    tag_names = {t for t in [tag1, tag2, tag3] if t}
    matched_tag_ids = {tag.id for tag in forum.available_tags if tag.name in tag_names}

    if not isinstance(forum, discord.ForumChannel):
        await interaction.followup.send(f"❌ Channel yang dipilih bukan forum")
    for thread in forum.threads:
        if keyword.lower() in thread.name.lower():
            thread_tag_ids = {tag.id for tag in thread.applied_tags}
            common_items = {id for id in thread_tag_ids if id in matched_tag_ids}
            if any(common_items):
                results.append(thread)

    if not results:
        await interaction.followup.send(f"❌ Tidak ditemukan pertanyaan dengan keyword: `{keyword}`", ephemeral=True)
        return

    hasil = f"🔍 **Hasil pencarian untuk:** `{keyword}`\n"
    for t in results[:10]:
        hasil += f"- [{t.name}]({t.jump_url})\n"

    await interaction.followup.send(hasil, ephemeral=True)
