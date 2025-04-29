import discord
from discord import app_commands
from data.all_channel_ids import Channel_IDs
from utils.function.autocomplete import hashtags
from utils.function.autocomplete import hashtags_filtered
forum_channel_id = Channel_IDs.discussion_threads.value  # Ganti dengan ID forum channel kamu

# Slash command utama
@app_commands.describe(
    discuss="Tulis topik diskusi atau pertanyaanmu (maksimal 100 karakter)",
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
async def discuss_command(
    interaction: discord.Interaction,
    discuss: str,
    device: str,
    software: str,
    topic: str,
    additional1: str = None,
    additional2: str = None
):
    forum_channel = interaction.client.get_channel(forum_channel_id)

    if not isinstance(forum_channel, discord.ForumChannel):
        await interaction.response.send_message("❌ Forum channel tidak ditemukan atau bukan forum.", ephemeral=True)
        return

    thread_tags = []
    unanswered_tags = discord.utils.get(forum_channel.available_tags, name="Unanswered")
    
    thread_tags.append(unanswered_tags)
    
    post_content = f"{interaction.user.mention} bertanya:\n**`{discuss}`** \n#{device} #{software} #{topic}"
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

        await interaction.response.send_message(f"✅ Pertanyaan kamu dipost di: {post.thread.mention}", ephemeral=True)

        await interaction.channel.send(
            f"📣 @everyone Pertanyaan baru dari {interaction.user.mention}!\n"
            f":question: Q: **`{discuss}`**\n\n"
            f"🔗 Lihat thread: {post.thread.mention}"
        )

    except Exception as e:
        await interaction.response.send_message(f"❌ Gagal membuat post: {str(e)}", ephemeral=True)
