import discord
from discord import app_commands
from discord.ext import commands
from data.all_channel_ids import Channel_IDs
from utils.function.autocomplete import hashtags
from utils.function.autocomplete import hashtags_filtered
forum_id = Channel_IDs.discussion_threads.value

def count_common_items(list1, list2):
    """
    Counts the number of common items between two lists, considering duplicates.

    Args:
        list1: The first list.
        list2: The second list.

    Returns:
        The number of common items.
    """
    count = 0
    temp_list2 = list2[:]  # Create a copy to avoid modifying the original list
    for item in list1:
        if item in temp_list2:
            count += 1
            temp_list2.remove(item)  # Remove the matched item to handle duplicates correctly
    return count
    
# Slash command utama
@app_commands.describe(
    keyword="Keyword yang ingin dicari",
    device="Tag device",
    software="Tag software",
    topic="Tag topic",
    additional1="(opsional)",
    additional2="(opsional)"
)
@app_commands.autocomplete(
    device=hashtags("device"),
    software=hashtags_filtered("software","device"),
    topic=hashtags("topic")
)
async def search_command(
    interaction: discord.Interaction, 
    keyword: str,
    device: str = None,
    software: str = None,
    topic: str = None,
    additional1: str = None,
    additional2: str = None):
    
    await interaction.response.defer(ephemeral=True, thinking=True)

    results = []
    results_matchedcount = []
    forum = interaction.client.get_channel(forum_id)
    
    hashtags_filter = []
    if device is not None:
        hashtags_filter.append(device)
    if software is not None:
        hashtags_filter.append(software)
    if topic is not None:
        hashtags_filter.append(topic)
    if additional1 is not None:
        hashtags_filter.append(additional1)
    if additional2 is not None:
        hashtags_filter.append(additional2)

    if not isinstance(forum, discord.ForumChannel):
        await interaction.followup.send(f"❌ Channel yang dipilih bukan forum")
       
    for thread in forum.threads:
        starter_message = await thread.fetch_message(thread.id)
        question = starter_message.content.split("bertanya:\n", 1)[1]
        question_hashtags_raw = question.split("\n#", 1)[1]
        question_hashtags = question_hashtags_raw.split(" #")
        matched_hashtags_count = count_common_items(question_hashtags,hashtags_filter)    
        if keyword.lower() in question.lower():
            if not thread in results:
                results.append(thread)    
                results_matchedcount.append(matched_hashtags_count)

    results_sorted = [thread for count, thread in sorted(zip(results_matchedcount, results), key=lambda pair: pair[0], reverse=True)]
         
    if not results:
        await interaction.followup.send("❌ Tidak ditemukan thread serupa", ephemeral=True)
        return
    
    hasil = f"Keyword: **{keyword}**\n"
    hasil += f"Tag: #{device} #{software} #{topic}"
    if additional1 is not None:
        hasil += f" #{additional1}"
    if additional2 is not None:
        hasil += f" #{additional2}"
    hasil += "\n"
    
    hasil += f"🔍 Hasil pencarian thread serupa:\n"
    
    for t in results_sorted[:10]:
        hasil += f"- {t.mention}\n"
        starter_message = await t.fetch_message(t.id)
        question = starter_message.content.split("bertanya:\n", 1)[1]
        hasil += f"{question}\n\n"
    
    await interaction.followup.send(hasil, ephemeral=True)
