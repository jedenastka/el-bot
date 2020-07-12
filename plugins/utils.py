from discord.ext import commands

@commands.command(name='ping')
async def c_ping(ctx):
    await ctx.send('Pong!')

def setup(bot):
    bot.add_command(c_ping)