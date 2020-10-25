async def c_ping(ctx):
    await ctx.send('Pong!')

async def readyMessage(ctx):
    print("Ready!")

events = [
    {
        'type': 'command',
        'name': 'ping',
        'aliases': ['test'],
        'callable': c_ping
    },
    {
        'type': 'onReady',
        'callable': readyMessage
    }
]