async def c_ping(ctx):
    await ctx.send('Pong!')
    print(f"{ctx.message.author} {ctx.message.guild.get_member(ctx.message.author.id)}")

events = [
    {
        'type': 'command',
        'name': 'ping',
        'aliases': ['test'],
        'callable': c_ping
    }
]