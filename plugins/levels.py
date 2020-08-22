import discord

from botutils import updateServerDoc, getServerDoc

def addXp(userId: int, serverId: int, xp: int):
    currentXp = getXp(userId, serverId)
    xp += currentXp if currentXp != {} else 0
    updateServerDoc(serverId, xp, ['plugins', 'levels', 'xp', str(userId)])

def getXp(userId: int, serverId: int):
    return getServerDoc(serverId, ['plugins', 'levels', 'xp', str(userId)])

async def c_levels(ctx, user=None):
    if user is None:
        user = ctx.message.author.id
    else:
        user = int(user)
    
    xp = getXp(ctx.message.guild.id, user)
    if xp == {}:
        await ctx.send(f"Invalid user {user}.")
        return
    await ctx.send(f"XP: {xp}")

async def c_levels_leaderboard(ctx):
    usersXp = getServerDoc(ctx.message.guild.id, ['plugins', 'levels', 'xp'])
    usersXp = {k: v for k, v in sorted(usersXp.items(), key=lambda item: item[1], reverse=True)}
    result = ''
    for userId, xp in usersXp.items():
        user = ctx.message.guild.get_member(int(userId))
        result += f"{user.name if user is not None else userId} - {xp}\n"
    await ctx.send(result)


async def c_levels_reeval(ctx):
    usersXp = {}
    statusMsg = await ctx.send('Initializing...')
    for channel in ctx.message.guild.text_channels:
        await statusMsg.edit(content=f"Reevaluating channel `{channel.name}`...")
        try:
            async for message in channel.history(limit=None):
                userId = message.author.id
                if usersXp.get(userId) is None:
                    usersXp[userId] = 0
                usersXp[userId] += len(message.content)
        except discord.Forbidden:
            pass
    await statusMsg.edit(content='Done!')
    updateServerDoc(ctx.message.guild.id, usersXp, ['plugins', 'levels', 'xp'])

async def messageLevel(ctx):
    addXp(ctx.message.author.id, ctx.message.guild.id, len(ctx.message.content))

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