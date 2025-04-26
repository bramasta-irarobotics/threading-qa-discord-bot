import discord
from discord import app_commands
from data.all_channel_ids import Channel_IDs
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
    tag1="Tag pertama",
    tag2="Tag kedua (opsional)",
    tag3="Tag ketiga (opsional)"
)
@app_commands.autocomplete(tag1=autocomplete_tags, tag2=autocomplete_tags, tag3=autocomplete_tags)
async def ask_command(
    interaction: discord.Interaction,
    discuss: str,
    tag1: str,
    tag2: str = None,
    tag3: str = None
):
    forum_channel = interaction.client.get_channel(FORUM_CHANNEL_ID)

    if not isinstance(forum_channel, discord.ForumChannel):
        await interaction.response.send_message("❌ Forum channel tidak ditemukan atau bukan forum.", ephemeral=True)
        return

    tag_names = {t for t in [tag1, tag2, tag3] if t}
    matched_tags = [tag for tag in forum_channel.available_tags if tag.name in tag_names]

    if not matched_tags:
        await interaction.response.send_message("❌ Tidak ada tag yang valid ditemukan.", ephemeral=True)
        return

    try:
        post = await forum_channel.create_thread(
            name=discuss[:100],
            content=f"{interaction.user.mention} bertanya:\n{discuss}",
            applied_tags=matched_tags
        )

        await interaction.response.send_message(f"✅ Pertanyaan kamu dipost di: {post.thread.mention}", ephemeral=True)

        await interaction.channel.send(
            f"📣 @everyone Pertanyaan baru dari {interaction.user.mention}!\n"
            f":discuss: Q: **`{discuss}`**\n\n"
            f"🔗 Lihat thread: {post.thread.mention}"
        )

    except Exception as e:
        await interaction.response.send_message(f"❌ Gagal membuat post: {str(e)}", ephemeral=True)
