import discord

ANNOUNCEMENT_CHANNEL_ID = 1359738837227798548

async def handle_reaction_add(bot, payload):
    if payload.user_id == bot.user.id:
        return

    VALID_EMOJI = "✅"
    if str(payload.emoji.name) != VALID_EMOJI:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if not member.guild_permissions.manage_messages:
        return

    channel = bot.get_channel(payload.channel_id)
    if not isinstance(channel, discord.Thread):
        return

    message = await channel.fetch_message(payload.message_id)
    forum = channel.parent
    tag = discord.utils.get(forum.available_tags, name="Answered")

    if tag is None:
        return

    await channel.edit(archived=False, locked=False, applied_tags=[tag])
    await channel.send(f"✅ Jawaban oleh {message.author.mention} telah disetujui oleh {member.mention}:\n{message.content}")

    announcement_channel = bot.get_channel(ANNOUNCEMENT_CHANNEL_ID)
    if announcement_channel:
        starter_message = await channel.fetch_message(channel.id)
        questioner = starter_message.mentions[0] if starter_message.mentions else starter_message.author
        question = starter_message.content.split("bertanya:\n", 1)[1]
        await announcement_channel.send(
            f"📌 Thread oleh {questioner.mention} di kategori `{forum.name}` telah **terjawab**!\n"
            f"✅ Jawaban telah divalidasi oleh {member.mention}.\n"
            f":question: Q: **`{question}`**\n"
            f":speech_balloon: A: **`{message.content}`**\n\n"
            f"🔗 Lihat thread: {channel.mention}"
        )
