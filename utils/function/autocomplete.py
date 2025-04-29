import discord
from discord import app_commands
from discord.ext import commands
from data.all_channel_ids import Channel_IDs
from data.all_tags import Tag_Class
forum_id = Channel_IDs.discussion_threads.value

# Fungsi autocomplete tag dengan filter nama
async def autocomplete_tags(
    interaction: discord.Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    forum_channel = interaction.client.get_channel(forum_id)

    if not isinstance(forum_channel, discord.ForumChannel):
        return []

    # Nama tag yang dilarang
    blocked_tag_names = ["Answered", "Unanswered"]

    filtered_tags = []
    for tag in forum_channel.available_tags:

        if (
            tag.name not in blocked_tag_names and
            current.lower() in tag.name.lower()
        ):
            filtered_tags.append(app_commands.Choice(name=tag.name, value=tag.name))

    return filtered_tags[:25]

# Fungsi autocomplete tag dengan emoji allowed sebagai parameter dari luar
def autocomplete_tags_filtered(allowed_emoji_name: str,source_option_name: str):
    async def autocomplete_tags_2(
        interaction: discord.Interaction,
        current: str
    ) -> list[app_commands.Choice[str]]:
        forum_channel = interaction.client.get_channel(forum_id)
        
        # Ambil nilai category dari input user
        category_value = getattr(interaction.namespace, source_option_name, None)
        if category_value is None:
            category_value = ""

        if not isinstance(forum_channel, discord.ForumChannel):
            return []

        blocked_tag_names = ["Answered", "Unanswered"]

        filtered_tags = []
        for tag in forum_channel.available_tags:
            emoji = tag.emoji.name if tag.emoji else None

            if (
                emoji == allowed_emoji_name and
                category_value.lower() in tag.name.lower() and
                tag.name not in blocked_tag_names and
                current.lower() in tag.name.lower()
            ):
                filtered_tags.append(app_commands.Choice(name=tag.name, value=tag.name))

        return filtered_tags[:25]
    return autocomplete_tags_2

# Fungsi autocomplete hashtag
def hashtags(tag_class: str):
    async def hashtags_autocomplete(
        interaction: discord.Interaction,
        current: str
    ) -> list[app_commands.Choice[str]]:
        forum_channel = interaction.client.get_channel(forum_id)      

        if not isinstance(forum_channel, discord.ForumChannel):
            return []

        hashtags = []
        for hashtag in Tag_Class[tag_class].value:
            if (
                current.lower() in hashtag.lower()
            ):
                hashtags.append(app_commands.Choice(name=hashtag, value=hashtag))

        return hashtags[:25]
    return hashtags_autocomplete

# Fungsi autocomplete hashtag with filtered keyword from other option
def hashtags_filtered(tag_class: str, source_option_name: str):
    async def hashtags_autocomplete_filtered(
        interaction: discord.Interaction,
        current: str
    ) -> list[app_commands.Choice[str]]:
        forum_channel = interaction.client.get_channel(forum_id)      

        if not isinstance(forum_channel, discord.ForumChannel):
            return []
            
        filter_value = getattr(interaction.namespace, source_option_name, None)

        filtered_hashtags = []
        for hashtag in Tag_Class[tag_class].value:
            if (
                filter_value.lower() in hashtag.lower() and
                current.lower() in hashtag.lower()
            ):
                filtered_hashtags.append(app_commands.Choice(name=hashtag, value=hashtag))

        return filtered_hashtags[:25]
    return hashtags_autocomplete_filtered