import datetime

import discord

import csplot

async def c_codestats(ctx, user = '', lastDays = 7):
    if user == '':
        user = ctx.message.author.name
    try:
        csplot.xpPlot(user, datetime.datetime.today() - datetime.timedelta(days=int(lastDays) - 1), f"tmp/codestats_{user}.png")
    except Exception:
        await ctx.send(f"There is no user {user}...")
    else:
        await ctx.send(file=discord.File(fp=open(f"tmp/codestats_{user}.png", 'rb')))

events = [
    {
        'type': 'command',
        'name': 'codestats',
        'aliases': ['cs'],
        'callable': c_codestats
    }
]