from discord.ext import commands
import json

with open('secrets.json') as f_secrets:
    secrets = json.load(f_secrets)

client = commands.Bot(command_prefix='eb!')

client.load_extension('plugins.utils')

client.run(secrets['token'])