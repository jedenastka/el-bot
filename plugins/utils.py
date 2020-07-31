async def c_ping(ctx, text = 'Pong!'):
    await ctx.message.channel.send(text)

async def foo(ctx, arg = ""):
    await ctx.message.channel.send(f"foo {arg}")

async def bar(ctx, arg = ""):
    await ctx.message.channel.send(f"bar {arg}")

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