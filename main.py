from discord.ext import commands
import json
from pymongo import MongoClient

with open('secrets.json') as f_secrets:
    secrets = json.load(f_secrets)

def prefix(bot, message):
    return bot.db['servers'].find_one({'_id': 'default'})['prefixes']

bot = commands.Bot(command_prefix=prefix)

mongo = MongoClient(secrets['mongoURI'])
bot.db = mongo['el']

bot.load_extension('plugins.utils')

bot.run(secrets['token'])