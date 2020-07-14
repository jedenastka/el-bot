import discord

from pymongo import MongoClient

import json
import importlib

from models import Context

# Load configuration files

with open('settings.json') as f_settings:
    settings = json.load(f_settings)

with open(settings['secretsFile']) as f_secrets:
    secrets = json.load(f_secrets)

# Initialize Discord client

bot = discord.Client()

# Initialize database

mongo = MongoClient(secrets['mongoURI'])
bot.db = mongo[settings['database']]

# Load plugins

events = []
plugins = settings['initPlugins']

for pluginName in plugins:
    plugin = importlib.import_module(f"{settings['pluginDir']}.{pluginName}")
    events += plugin.events

# Helper functions

def splitNoBreak(string: str):
    splittedString = []
    tmp = ''
    inQuotes = False

    for i in range(len(string)):
        ch = string[i]
        previousCh = string[i - 1] if i != 0 else ''
        nextCh = string[i + 1] if i != len(string) - 1 else ''
        chIsQuote = False
        
        if ch in ('"', '\''):
            if not inQuotes and previousCh == ' ':
                inQuotes = True
                chIsQuote = True
            elif inQuotes and nextCh in (' ', ''):
                inQuotes = False
                chIsQuote = True
        
        if (ch != ' ' or inQuotes) and not chIsQuote:
            tmp += ch
        
        if (ch == ' ' and not inQuotes) or nextCh == '':
            splittedString.append(tmp)
            tmp = ''
        
        if nextCh == '' and inQuotes:
            raise Exception('Unclosed quote')
    
    return splittedString

def getPrefix(message, all=False):
    prefixes = bot.db['servers'].find_one({'_id': 'default'})['prefixes']
    if all:
        return prefixes
    for prefix in prefixes:
        if message.content.startswith(prefix):
            return prefix
    return None

def getCommand(message, event):
    prefix = getPrefix(message)
    if prefix is not None:
        commandString = message.content[len(prefix):]

        try:
            splittedCommand = splitNoBreak(commandString)
        except Exception:
            return None

        command = {
            'command': splittedCommand[0],
            'args': splittedCommand[1:]
        }

        return command

    return None

# Listen on Discord events and pass them to registered internal events

@bot.event
async def on_message(message):
    context = Context(message, bot)

    for event in events:

        if event['type'] == 'command':
            command = getCommand(message, event)
            if command is not None:
                if command['command'] in event['alias'] + [event['name']]:
                    await event['callable'](context, *command['args'])
        
        elif event['type'] == 'onMessage':
            await event['callable'](context)

# Run the bot

bot.run(secrets['token'])