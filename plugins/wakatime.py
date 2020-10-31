import datetime
import io
import re

import requests

import discord

from botutils import getServerDoc

dbPath = ['plugins', 'wakatime']

async def c_wakatime(ctx, user=None):
    if user is None:
        user = ctx.message.author.name
    
    profile = getServerDoc(ctx.message.guild.id, dbPath + ['profiles', str(user)], addOverlay=True)
    if profile == {}:
        return
    
    now = datetime.datetime.now()
    
    r = requests.get(f"https://wakatime.com/share/@{profile['id']}/{profile['chart']}?{int(now.timestamp())}")
    
    ext = re.match(r'.*(\..+)', profile['chart']).group(1)

    await ctx.send(file=discord.File(io.BytesIO(r.content), filename=f"{int(now.timestamp())}.{ext}"))

events = [
    {
        'type': 'command',
        'name': 'wakatime',
        'aliases': ['waka'],
        'callable': c_wakatime
    }
]