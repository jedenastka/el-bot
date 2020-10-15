from botutils import getServerDoc

async def checkCounting(ctx):
    if ctx.message.channel.id in getServerDoc(ctx.message.guild.id, ['plugins', 'counting', 'channels']):
        lastMsg = await ctx.message.channel.history(limit=2).flatten()
        lastMsg = lastMsg[1]
        if not isinstance(ctx.message.content, int) or int(ctx.message.content) != int(lastMsg.content) + 1 or ctx.message.author.id == lastMsg.author.id:
            await ctx.message.delete()

events = [
    {
        'type': 'onMessage',
        'callable': checkCounting
    }
]