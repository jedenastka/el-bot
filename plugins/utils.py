async def c_ping(ctx):
    await ctx.message.channel.send('Pong!')

events = [
    {
        'type': 'command',
        'name': 'ping',
        'aliases': ['test'],
        'callable': c_ping
    }
]