import importlib
import sys
import os

from instances import bot, db, settings, secrets, events
from event_handlers import on_message, on_message_delete, on_message_edit, on_raw_reaction_add, on_raw_reaction_remove, on_guild_join, on_ready

import discord

# Load plugins

sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/..")

plugins = settings['initPlugins']

for pluginName in plugins:
    plugin = importlib.import_module(f"{settings['pluginDir']}.{pluginName}")
    events += plugin.events

# Register event handlers

bot.event(on_message)
bot.event(on_message_delete)
bot.event(on_message_edit)
bot.event(on_raw_reaction_add)
bot.event(on_raw_reaction_remove)
bot.event(on_guild_join)
bot.event(on_ready)

# Run the bot

bot.run(secrets['token'])