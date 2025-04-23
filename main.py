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

# Import event modules
from events.forum.reaction_add import handle_reaction_add
from utils.bot.ready import on_ready_event

# Register slash commands
bot.tree.command(name="ask", description="Ajukan pertanyaan berdasarkan topik")(ask_command)
bot.tree.command(name="get_channel_ids", description="Ambil semua ID forum channel di server ini")(get_channel_ids_command)
bot.tree.command(name="search", description="Cari pertanyaan berdasarkan keyword (judul thread)")(search_command)
bot.tree.command(name="ping", description="Ping test")(ping_command)

# Register event handlers
@bot.event
async def on_raw_reaction_add(payload):
    await handle_reaction_add(bot, payload)

@bot.event
async def on_ready():
    await on_ready_event(bot)


# Run the bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
