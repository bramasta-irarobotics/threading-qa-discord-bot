# === main.py ===
from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# import data modules
from utils.bot.bot_setup import bot
from data.categories import CATEGORY_TO_CHANNEL

# Import command modules
from commands.user.ask import ask_command
from commands.admin.get_channel_ids import get_channel_ids_command
from commands.user.search import search_command
from commands.user.ping import ping_command
#from commands.user.result import result_command
#from commands.user.close import close_command

# Import event modules
from events.forum.reaction_add import handle_reaction_add
from utils.bot.ready import on_ready_event
#from events.forum.on_message import handle_on_message

# Register slash commands
bot.tree.command(name="ask", description="Ajukan pertanyaan berdasarkan topik")(ask_command)
bot.tree.command(name="get_channel_ids", description="Ambil semua ID forum channel di server ini")(get_channel_ids_command)
bot.tree.command(name="search", description="Cari pertanyaan berdasarkan keyword (judul thread)")(search_command)
bot.tree.command(name="ping", description="Ping test")(ping_command)
#bot.tree.command(name="result", description="Lihat peringkat jawaban di thread ini berdasarkan jumlah 👍")(result_command)
#bot.tree.command(name="close", description="Tutup thread ini jika sudah selesai")(close_command)

# Register event handlers
@bot.event
async def on_raw_reaction_add(payload):
    await handle_reaction_add(bot, payload)

@bot.event
async def on_ready():
    await on_ready_event(bot)

#@bot.event
#async def on_message(message):
#    await handle_on_message(bot, message)


# Run the bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
