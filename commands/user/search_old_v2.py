import discord
from discord import app_commands
from discord.ext import commands
from data.all_channel_ids import Channel_IDs
from utils.function.autocomplete import autocomplete_tags
from utils.function.autocomplete import autocomplete_tags_filtered
forum_id = Channel_IDs.discussion_threads.value

# Slash command utama
@app_commands.describe(
    keyword="Keyword yang ingin dicari",
    tag1="Tag pertama (opsional)",
    tag2="Tag kedua (opsional)",
    tag3="Tag ketiga (opsional)",
    tag4="Tag keempat (opsional)",
    tag5="Tag kelima (opsional)",
)
@app_commands.autocomplete(tag1=autocomplete_tags, tag2=autocomplete_tags_filtered("⚙️","tag1"), tag3=autocomplete_tags, tag4=autocomplete_tags, tag5=autocomplete_tags)
async def search_command(
    interaction: discord.Interaction, 
    keyword: str,
    tag1: str = None,
    tag2: str = None,
    tag3: str = None,
    tag4: str = None,
    tag5: str = None):
    
    await interaction.response.defer(ephemeral=True, thinking=True)

    results = []
    forum = interaction.client.get_channel(forum_id)
    
    tag_names = {t for t in [tag1, tag2, tag3, tag4, tag5] if t}
    matched_tag_ids = {tag.id for tag in forum.available_tags if tag.name in tag_names}

    if not isinstance(forum, discord.ForumChannel):
        await interaction.followup.send(f"❌ Channel yang dipilih bukan forum")
    for i in range(5,-1,-1):
        for thread in forum.threads:
            if keyword.lower() in thread.name.lower():
                thread_tag_ids = {tag.id for tag in thread.applied_tags}
                common_tags = {id for id in thread_tag_ids if id in matched_tag_ids}
                if len(common_tags)==i:
                    if not thread in results:
                        results.append(thread)
                
    if not results:
        await interaction.followup.send("❌ Tidak ditemukan thread serupa", ephemeral=True)
        return
    
    hasil = f"Keyword: **{keyword}**\nTag:"
    
    first_iteration = True
    for tag in tag_names:
        if first_iteration:
            hasil += f" `{tag}`"
        else:
            hasil += f", `{tag}`"
        first_iteration = False
    hasil += "\n"
    hasil += f"🔍 Hasil pencarian thread serupa:\n"
    
    for t in results[:10]:
        hasil += f"- **{t.name}**\n"
        hasil += f"  Tag:"
        t_tag = {tag.name for tag in t.applied_tags}
        first_iteration = True
        for tag in t_tag:
            if first_iteration:
                hasil += f" `{tag}`"
            else:
                hasil += f", `{tag}`"
            first_iteration = False
        hasil += f"\n  Link thread: {t.mention}\n\n"
        
    #tag_emoji = {tag.emoji.name for tag in forum.available_tags if tag.name in tag_names}
    #for emoji in tag_emoji:
        #print(emoji == "⚙️")
        #hasil += f"{emoji}"

    await interaction.followup.send(hasil, ephemeral=True)
