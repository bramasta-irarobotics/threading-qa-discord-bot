import discord
from discord import app_commands
from discord.ext import commands
from data.categories import CATEGORY_TO_CHANNEL

@app_commands.describe(
    question="Tulis pertanyaanmu",
    category="Pilih kategori topik"
)
@app_commands.choices(category=[
    app_commands.Choice(name="programming-standard", value="programming-standard"),
    app_commands.Choice(name="vane", value="vane"),
    app_commands.Choice(name="robot-abb", value="robot-abb")
])
async def ask_command(interaction: discord.Interaction, question: str, category: app_commands.Choice[str]):
    forum_channel_id = CATEGORY_TO_CHANNEL.get(category.value)
    forum_channel = interaction.client.get_channel(forum_channel_id)

    if not isinstance(forum_channel, discord.ForumChannel):
        await interaction.response.send_message("❌ Forum channel tidak ditemukan untuk kategori ini.", ephemeral=True)
        return

    tag = discord.utils.get(forum_channel.available_tags, name="Unanswered")
    if tag is None:
        await interaction.response.send_message("❌ Tag 'Unanswered' tidak ditemukan.", ephemeral=True)
        return

    try:
        post = await forum_channel.create_thread(
            name=question[:100],
            content=f"{interaction.user.mention} bertanya:\n{question}",
            applied_tags=[tag]
        )

        await interaction.response.send_message(f"✅ Pertanyaan kamu dipost di: {post.thread.mention}", ephemeral=True)

        await interaction.channel.send(
            f"📣 @everyone Pertanyaan baru dari {interaction.user.mention} di kategori `{category.name}`!\n"
            f":question: Q: **`{question}`**\n\n"
            f"🔗 Lihat thread: {post.thread.mention}"
        )

    except Exception as e:
        await interaction.response.send_message(f"❌ Gagal membuat post: {str(e)}", ephemeral=True)
