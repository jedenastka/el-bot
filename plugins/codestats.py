import datetime
import os

import discord

import csplot

os.makedirs('fs/tmp/codestats', exist_ok=True)

async def c_codestats(ctx, user = '', lastDays = 7):
    if user == '':
        user = ctx.message.author.name
    try:
        csplot.xpPlot(user, datetime.datetime.today() - datetime.timedelta(days=int(lastDays) - 1), f"fs/tmp/codestats/{user}.png")
    except Exception:
        await ctx.send(f"There is no user {user}...")
    else:
        await ctx.send(file=discord.File(fp=open(f"fs/tmp/codestats/{user}.png", 'rb')))

events = [
    {
        'type': 'command',
        'name': 'codestats',
        'aliases': ['cs'],
        'callable': c_codestats
    }
]