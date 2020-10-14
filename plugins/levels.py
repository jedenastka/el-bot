import math

import discord

from botutils import updateServerDoc, getServerDoc, awaitIfAwaitable, createEmbed

def addXp(userId: int, serverId: int, xp: int):
    currentXp = getXp(userId, serverId)
    xp += currentXp if currentXp != {} else 0
    updateServerDoc(serverId, xp, ['plugins', 'levels', 'xp', str(userId)])

def getXp(userId: int, serverId: int):
    return getServerDoc(serverId, ['plugins', 'levels', 'xp', str(userId)])

async def reevaluate(server, statusFunction=print, sendStatusEvery=500):
    await awaitIfAwaitable(statusFunction, 'Initializing...')

    usersXp = {}
    for channel in server.text_channels:
        await awaitIfAwaitable(statusFunction, f"Reevaluating channel `{channel.name}`...")
        
        try:
            i = 1
            async for message in channel.history(limit=None):
                userId = message.author.id
                if usersXp.get(str(userId)) is None:
                    usersXp[str(userId)] = 0
                usersXp[str(userId)] += len(message.content)
                if i % sendStatusEvery == 0:
                    await awaitIfAwaitable(statusFunction, f"Reevaluating channel `{channel.name}` ({i} ±{sendStatusEvery} messages so far)...")
                    pass
                i += 1
        except discord.Forbidden:
            pass

    await awaitIfAwaitable(statusFunction, 'Writing to database...')
    updateServerDoc(server.id, usersXp, ['plugins', 'levels', 'xp'])
    await awaitIfAwaitable(statusFunction, 'Done!')

def xpToLevel(xp: int):
    base = 2
    hardness = 100
    return math.floor((xp / hardness) ** (1 / base))

def levelToXp(level: int):
    base = 2
    hardness = 100
    return (math.floor(level) ** base) * hardness

def userPlace(userId: int, guildId: int):
    usersXp = getServerDoc(guildId, ['plugins', 'levels', 'xp'])
    usersXp = {k: v for k, v in sorted(usersXp.items(), key=lambda item: item[1], reverse=True)}

    return list(usersXp.keys()).index(str(userId)) + 1

async def c_levels(ctx, user=None):
    if user is None:
        user = ctx.message.author
    else:
        userId = user
        user = ctx.message.guild.get_member(int(userId))
        if user is None:
            await ctx.send(f"Invalid user {userId}.")
    
    xp = getXp(user.id, ctx.message.guild.id)
    if xp == {}:
        await ctx.send(f"{user.name} is not in the database.")
        return
    
    await ctx.send(f"[{userPlace(user.id, ctx.message.guild.id)}] **{user.name}**: {xpToLevel(xp)} ({xp})")

async def c_levels_leaderboard(ctx, page=1):
    page = int(page)
    perPage = 10

    usersXp = getServerDoc(ctx.message.guild.id, ['plugins', 'levels', 'xp'])
    usersXp = {k: v for k, v in sorted(usersXp.items(), key=lambda item: item[1], reverse=True)}

    result = ''
    for i in range((page - 1) * perPage, page * perPage):
        if i >= len(usersXp):
            break
        
        userId, xp = list(usersXp.items())[i]
        user = ctx.message.guild.get_member(int(userId))
        result += f"[{i + 1}] **{user.name if user is not None else userId}**: {xpToLevel(xp)} ({xp})\n"
        i += 1
    await ctx.send(result)


async def c_levels_reeval(ctx):
    statusMsg = await ctx.send('Waiting for status...')

    async def statusFunction(status: str):
        await statusMsg.edit(content=status)

    await reevaluate(ctx.message.guild, statusFunction)

async def messageLevel(ctx):
    oldLevel = xpToLevel(getXp(ctx.message.author.id, ctx.message.guild.id))
    
    addXp(ctx.message.author.id, ctx.message.guild.id, len(ctx.message.content))
    
    newLevel = xpToLevel(getXp(ctx.message.author.id, ctx.message.guild.id))

    if newLevel > oldLevel:
        await ctx.send(f"{ctx.message.author.name} leveled up! **{oldLevel}** :arrow_right: **{newLevel}**")

events = [
    {
        'type': 'command',
        'name': 'levels',
        'aliases': ['lvl', 'xp'],
        'callable': c_levels,
        'subcommands': [
            {
                'type': 'command',
                'name': 'reeval',
                'aliases': [],
                'callable': c_levels_reeval
            },
            {
                'type': 'command',
                'name': 'leaderboard',
                'aliases': [],
                'callable': c_levels_leaderboard
            }
        ]
    },
    {
        'type': 'onMessage',
        'callable': messageLevel
    }
]