import discord
from discord import app_commands
from discord.ext import commands

# Setup Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.guild_messages = True
intents.reactions = True
intents.members = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)
