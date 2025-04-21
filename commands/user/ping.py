import discord

async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")
