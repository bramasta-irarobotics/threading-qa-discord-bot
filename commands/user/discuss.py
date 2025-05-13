import discord
from discord import app_commands
from data.all_channel_ids import Channel_Names_to_IDs
from utils.function.autocomplete import hashtags
from utils.function.autocomplete import hashtags_filtered

# Slash command utama
@app_commands.describe(
    discuss="Tulis topik diskusi atau pertanyaanmu (maksimal 100 karakter)",
    topic="Jenis topik diskusi",
    device="Tag device",
    software="Tag software",
    additional1="(opsional)",
    additional2="(opsional)"
)
#=== /ask choices ===
@app_commands.choices(topic=[
    app_commands.Choice(name="discussion-threads", value="discussion-threads")
])
@app_commands.autocomplete(
    device=hashtags("device"),
    software=hashtags_filtered("software","device")
)
async def discuss_command(
    interaction: discord.Interaction,
    discuss: str,
    topic: app_commands.Choice[str],
    device: str,
    software: str,
    additional1: str = None,
    additional2: str = None
):
    forum_channel_id = Channel_Names_to_IDs.get(topic.value)
    forum_channel = interaction.client.get_channel(forum_channel_id)

    if not isinstance(forum_channel, discord.ForumChannel):
        await interaction.response.send_message("❌ Forum channel tidak ditemukan atau bukan forum.", ephemeral=True)
        return

    thread_tags = []
    unanswered_tags = discord.utils.get(forum_channel.available_tags, name="Unanswered")
    
    thread_tags.append(unanswered_tags)
    
    post_content = f"{interaction.user.mention} :\n**`{discuss}`** \n#{device} #{software}"
    if additional1 is not None:
        post_content += f" #{additional1}"
    if additional2 is not None:
        post_content += f" #{additional2}"

    if not thread_tags:
        await interaction.response.send_message("❌ Tidak ada tag yang valid ditemukan.", ephemeral=True)
        return

    try:
        post = await forum_channel.create_thread(
            name=discuss[:100],
            content=post_content,
            applied_tags=thread_tags
        )

        #await interaction.response.send_message(f"✅ Diskusi kamu dipost di: {post.thread.mention}", ephemeral=True)

        await interaction.channel.send(
            f"📣 @everyone Diskusi/Pengumuman baru dari {interaction.user.mention}!\n"
            f":thought_balloon: **`{discuss}`**\n\n"
            f"🔗 Lihat thread: {post.thread.mention}"
        )

    except Exception as e:
        await interaction.response.send_message(f"❌ Gagal membuat post: {str(e)}", ephemeral=True)
