import discord
from discord import app_commands
from data.all_channel_ids import Channel_IDs
from utils.function.autocomplete import hashtags_filtered
FORUM_CHANNEL_ID = Channel_IDs.discussion_threads.value  # Ganti dengan ID forum channel kamu

# Fungsi autocomplete tag
async def autocomplete_tags(
    interaction: discord.Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    forum_channel = interaction.client.get_channel(FORUM_CHANNEL_ID)

    if not isinstance(forum_channel, discord.ForumChannel):
        return []

    return [
        app_commands.Choice(name=tag.name, value=tag.name)
        for tag in forum_channel.available_tags
        if current.lower() in tag.name.lower()
    ][:25]  # Max 25 pilihan sesuai limit Discord

# Slash command utama
@app_commands.describe(
    discuss="Tulis topik diskusi atau pertanyaanmu",
    device="Tag device",
    software="Tag software",
    topic="Tag topic",
    additional1="(opsional)",
    additional2="(opsional)"
)
@app_commands.autocomplete(
    device=hashtags_filtered("device",""),
    software=autocomplete_tags,
    topic=autocomplete_tags,
    additional1=autocomplete_tags,
    additional2=autocomplete_tags
)
async def discuss_command(
    interaction: discord.Interaction,
    discuss: str,
    device: str,
    software: str,
    topic: str,
    additional1: str = None,
    additional2: str = None
):
    forum_channel = interaction.client.get_channel(FORUM_CHANNEL_ID)

    if not isinstance(forum_channel, discord.ForumChannel):
        await interaction.response.send_message("❌ Forum channel tidak ditemukan atau bukan forum.", ephemeral=True)
        return

    #tag_names = {t for t in [device, software, topic, additional1, additional2] if t}
    #matched_tags = [tag for tag in forum_channel.available_tags if tag.name in tag_names]
    thread_tags = [discord.utils.get(forum_channel.available_tags, name="Unanswered")]

    if not thread_tags:
        await interaction.response.send_message("❌ Tidak ada tag yang valid ditemukan.", ephemeral=True)
        return

    try:
        post = await forum_channel.create_thread(
            name=discuss[:100],
            content=f"{interaction.user.mention} bertanya:\n{discuss}",
            applied_tags=thread_tags
        )

        await interaction.response.send_message(f"✅ Pertanyaan kamu dipost di: {post.thread.mention}", ephemeral=True)

        await interaction.channel.send(
            f"📣 @everyone Pertanyaan baru dari {interaction.user.mention}!\n"
            f":discuss: Q: **`{discuss}`**\n\n"
            f"🔗 Lihat thread: {post.thread.mention}"
        )

    except Exception as e:
        await interaction.response.send_message(f"❌ Gagal membuat post: {str(e)}", ephemeral=True)
