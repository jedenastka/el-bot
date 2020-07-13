import discord

from pymongo import MongoClient

import json
import importlib

with open('settings.json') as f_settings:
    settings = json.load(f_settings)

with open(settings['secretsFile']) as f_secrets:
    secrets = json.load(f_secrets)

bot = discord.Client()

mongo = MongoClient(secrets['mongoURI'])
bot.db = mongo[settings['database']]

events = []
plugins = settings['initPlugins']

for pluginName in plugins:
    plugin = importlib.import_module(f"{settings['pluginDir']}.{pluginName}")
    events += plugin.events

def getCommand(message, event):
    prefixes = bot.db['servers'].find_one({'_id': 'default'})['prefixes']
    for prefix in prefixes:
        if message.content.startswith(prefix):
            commandString = message.content[len(prefix):]
            splittedCommand = commandString.split(' ')
            command = {
                'command': splittedCommand[0],
                'args': splittedCommand[1:]
            }
            return command
    return None

@bot.event
async def on_message(message):
    for event in events:
        if event['type'] == 'command':
            command = getCommand(message, event)
            if command is not None:
                if command['command'] in event['alias'] + [event['name']]:
                    await event['callable'](bot, message, *command['args'])
        elif event['type'] == 'onMessage':
            await event['callable'](bot, message)

bot.run(secrets['token'])