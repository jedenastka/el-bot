async def c_ping(ctx, text = 'Pong!'):
    await ctx.message.channel.send(text)

async def foo(ctx):
    await ctx.message.channel.send("foo")

async def bar(ctx):
    await ctx.message.channel.send("bar")

events = [
    {
        'type': 'command',
        'name': 'ping',
        'aliases': ['test'],
        'callable': c_ping
    },
    {
        'type': 'command',
        'name': 'foo',
        'aliases': [],
        'callable': foo,
        'subcommands': [
            {
                'type': 'command',
                'name': 'bar',
                'aliases': [],
                'callable': bar
            }
        ]
    }
]