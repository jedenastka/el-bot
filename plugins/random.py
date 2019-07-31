import discord
from discord.ext import commands
import random

"""
Name: random
Description: El Bot plugin for randomization.
Author: Grzesiek11
Version: v1.0.1
"""

class RandomPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Randomization commands
    @commands.group(name = 'random', aliases = ['rand', 'randomize'])
    async def _random(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    # Give a random number
    @_random.command(name = 'number', aliases = ['num'])
    async def _number(self, ctx, start : int, end : int):
        await ctx.send(random.randint(start, end))

    # Get a random choice from a set of things
    @_random.command(name = 'lottery', aliases = ['choice'])
    async def _lottery(self, ctx, *choices : str):
        await ctx.send(random.choice(choices))
    
    # Flip a coin
    @_random.command(name = 'coin', aliases = ['coinflip'])
    async def _coin(self, ctx):
        await ctx.send(f'''{random.choices(['Tails', 'Heads'])[0]}!''')

def setup(bot):
    bot.add_cog(RandomPlugin(bot))