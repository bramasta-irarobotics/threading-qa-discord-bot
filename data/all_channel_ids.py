from enum import Enum

class Channel_Names(Enum):
    moderator_only = "moderator-only"
    guidelines = "guidelines"
    general_topic = "general-topic"
    bot_status = "bot-status"
    ask_or_search = "ask-or-search"
    discussion_threads = "discussion-threads"

Channel_Names_to_IDs = {
    Channel_Names.moderator_only.value: 1365172459669557300,
    Channel_Names.guidelines.value: 1365172459669557302,
    Channel_Names.general_topic.value: 1365172459669557304,
    Channel_Names.bot_status.value: 1365172459669557305,
    Channel_Names.ask_or_search.value: 1365172459669557307,
    Channel_Names.discussion_threads.value: 1365172735541641216,
}

class Channel_IDs(Enum):
    moderator_only = 1365172459669557300
    guidelines = 1365172459669557302
    general_topic = 1365172459669557304
    bot_status = 1365172459669557305
    ask_or_search = 1365172459669557307
    discussion_threads = 1365172735541641216
