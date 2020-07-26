import datetime

import discord

import csplot

async def c_codestats(ctx, user: str, lastDays = 7):
    try:
        csplot.xpPlot(user, datetime.datetime.today() - datetime.timedelta(days=int(lastDays) - 1), f"tmp/codestats_{user}.png")
    except Exception:
        await ctx.message.channel.send(f"There is no user {user}...")
    finally:
        await ctx.message.channel.send(file=discord.File(fp=open(f"tmp/codestats_{user}.png", 'rb')))

events = [
    {
        'type': 'command',
        'name': 'codestats',
        'alias': ['cs'],
        'callable': c_codestats
    }
]