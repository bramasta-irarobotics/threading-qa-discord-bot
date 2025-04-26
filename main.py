# === main.py ===
from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# import data modules
from utils.bot.bot_setup import bot

# Import command modules
from commands.user.ask import ask_command
from commands.user.search import search_command
from commands.user.ping import ping_command
from commands.admin.get_channel_ids_forum import get_channel_ids_forum_command
from commands.admin.restart_bot import restart_bot_command
from commands.admin.shutdown_bot import shutdown_bot_command
from commands.admin.get_channel_ids_all import get_all_channel_ids_command
from commands.admin.refresh_commands import refresh_commands_command
from commands.admin.create_tag import create_tag_command

# Import event modules
from events.forum.reaction_add import handle_reaction_add
from utils.bot.ready import on_ready_event

# Register slash commands for user
bot.tree.command(name="discuss", description="Ajukan pertanyaan atau mulai diskusi baru")(ask_command)
bot.tree.command(name="search", description="Cari pertanyaan berdasarkan keyword (judul thread)")(search_command)
bot.tree.command(name="ping", description="Ping test")(ping_command)

# Register slash commands for admin
bot.tree.command(name="get_channel_ids_forum", description="Ambil semua ID forum channel di server ini")(get_channel_ids_forum_command)
bot.tree.command(name="get_channel_ids_all", description="Ambil semua ID channel di server ini")(get_all_channel_ids_command)
bot.tree.command(name="restart", description="Restart bot (hanya admin)")(restart_bot_command)
bot.tree.command(name="shutdown", description="Shutdown bot (hanya admin)")(shutdown_bot_command)
bot.tree.command(name="refresh_commands", description="Bersihkan dan sinkron ulang semua slash command")(refresh_commands_command)
bot.tree.command(name="create_tag", description="Buat Tag baru(hanya admin)")(create_tag_command)

# Register event handlers
@bot.event
async def on_raw_reaction_add(payload):
    await handle_reaction_add(bot, payload)

@bot.event
async def on_ready():
    await on_ready_event(bot)

# Run the bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))