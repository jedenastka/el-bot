import json

import discord

from pymongo import MongoClient

# Load configuration files

with open('settings.json') as f_settings:
    settings = json.load(f_settings)

with open(settings['secretsFile']) as f_secrets:
    secrets = json.load(f_secrets)

# Initialize Discord client

bot = discord.Client(intents=discord.Intents.all())

# Initialize database

mongo = MongoClient(secrets['mongoURI'])
db = mongo[settings['database']]

events = []