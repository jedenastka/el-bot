async def c_ping(ctx, text = 'Pong!'):
    await ctx.message.channel.send(text)

events = [
    {
        'type': 'command',
        'name': 'ping',
        'aliases': ['test'],
        'callable': c_ping
    }
]