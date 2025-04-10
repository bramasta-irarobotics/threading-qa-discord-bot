import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Ini penting!

# === Setup Bot ===
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# === Logging ke File ===
def log_event(event_type: str, user: str, content: str, extra: str = ""):
    with open("qa_logs.txt", "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{event_type}] [{timestamp}] {user}: {content}"
        if extra:
            line += f" ({extra})"
        log_file.write(line + "\n")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} commands.")
    except Exception as e:
        print(f"⚠️ Sync failed: {e}")

# === /ask ===
@bot.tree.command(name="ask", description="Ajukan pertanyaan Q&A")
@app_commands.describe(question="Tulis pertanyaan kamu di sini")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.send_message(f"❓ Pertanyaan dari {interaction.user.mention}: **{question}**", ephemeral=False)
    msg = await interaction.original_response()

    thread = await msg.create_thread(name=question[:90])
    await thread.send(f"{interaction.user.mention} telah mengajukan pertanyaan. Silakan jawab di sini!")

    # Log ke file
    log_event("QUESTION", interaction.user.name, question)

# === /accept ===
@bot.tree.command(name="accept", description="Tandai jawaban sebagai yang diterima")
@app_commands.describe(message_link="Link ke pesan yang ingin ditandai")
async def accept(interaction: discord.Interaction, message_link: str):
    try:
        parts = message_link.split("/")
        channel_id = int(parts[5])
        message_id = int(parts[6])
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        await message.add_reaction("✅")
        await interaction.response.send_message(f"✅ Jawaban dari {message.author.mention} telah diterima!", ephemeral=False)

        if isinstance(channel, discord.Thread):
            new_name = f"✅ {channel.name}" if not channel.name.startswith("✅") else channel.name
            await channel.edit(name=new_name)

        # Log ke file
        log_event("ANSWER ACCEPTED", message.author.name, message.content, message_link)

    except Exception as e:
        print(f"Error: {e}")
        await interaction.response.send_message("❌ Gagal menandai jawaban.", ephemeral=True)

# === /votes ===
@bot.tree.command(name="votes", description="Lihat jumlah upvote dan downvote pada sebuah jawaban")
@app_commands.describe(message_link="Link ke jawaban yang ingin dicek")
async def votes(interaction: discord.Interaction, message_link: str):
    try:
        parts = message_link.split("/")
        channel_id = int(parts[5])
        message_id = int(parts[6])
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        upvotes = 0
        downvotes = 0
        for reaction in message.reactions:
            if reaction.emoji == "👍":
                upvotes = reaction.count - 1
            elif reaction.emoji == "👎":
                downvotes = reaction.count - 1

        await interaction.response.send_message(
            f"📊 Voting untuk jawaban:\n👍 Upvotes: {upvotes}\n👎 Downvotes: {downvotes}",
            ephemeral=True
        )
    except Exception as e:
        print(f"Error: {e}")
        await interaction.response.send_message("❌ Gagal mengambil voting.", ephemeral=True)

@bot.event
async def on_message(message):
    # Hindari respon terhadap pesan bot sendiri
    if message.author.bot:
        return

    # Cek jika pesan dikirim dalam thread
    if message.channel.type == discord.ChannelType.public_thread:
        # Bisa tambahkan pengecekan nama thread juga jika perlu
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    await bot.process_commands(message)  # Jangan lupa ini biar command tetap jalan

# === /result ===
@bot.tree.command(name="result", description="Lihat peringkat jawaban di thread ini berdasarkan jumlah 👍")
@app_commands.checks.has_permissions(send_messages=True)
async def result(interaction: discord.Interaction):
    if interaction.channel.type != discord.ChannelType.public_thread:
        await interaction.response.send_message("❌ Command ini hanya bisa digunakan di dalam thread pertanyaan.", ephemeral=True)
        return

    await interaction.response.defer(thinking=True)

    messages = [msg async for msg in interaction.channel.history(limit=100)]
    scored_messages = []

    for msg in messages:
        if msg.author.bot:
            continue  # Lewati bot
        for reaction in msg.reactions:
            if str(reaction.emoji) == "👍":
                scored_messages.append((msg, reaction.count))

    if not scored_messages:
        await interaction.followup.send("Belum ada jawaban dengan 👍 di thread ini.")
        return

    # Urutkan dari vote tertinggi ke terendah
    ranked = sorted(scored_messages, key=lambda x: x[1], reverse=True)

    hasil = "**📊 Ranking Jawaban Terbaik:**\n"
    for i, (msg, score) in enumerate(ranked[:5], start=1):
        hasil += f"**#{i}** – 👍 {score} – oleh {msg.author.mention}\n> {msg.content[:80]}...\n"

    await interaction.followup.send(hasil)

# === Jalankan Bot ===
bot.run(os.getenv("DISCORD_BOT_TOKEN"))  # Ganti dengan token bot kamu
