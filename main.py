import discord

from pymongo import MongoClient

import json
import importlib

with open('secrets.json') as f_secrets:
    secrets = json.load(f_secrets)

bot = discord.Client()

mongo = MongoClient(secrets['mongoURI'])
bot.db = mongo['el']

prefix = bot.db['servers'].find_one({'_id': 'default'})['prefixes'][0]

events = []
plugins = ['utils']

for pluginName in plugins:
    plugin = importlib.import_module(f"plugins.{pluginName}")
    events += plugin.events

@bot.event
async def on_message(message):
    for event in events:
        if event['type'] == 'command':
            if message.content.startswith(prefix): # Add some complex prefix getting based on various things here
                if message.content[len(prefix):] in event['alias'] + [event['name']]:
                    await event['callable'](bot, message)
        elif event['type'] == 'onMessage':
            await event['callable'](bot, message)

bot.run(secrets['token'])