import discord
from discord.ext import commands
import youtube_dl, os

"""
Name: util
Description: Various things not deserving own plugin.
Author: Grzesiek11
Version: v1.0.0
"""

class UtilPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'ping', aliases = ['test'])
    async def _ping(self, ctx):
        await ctx.send("Pong!")
    
def setup(bot):
    bot.add_cog(UtilPlugin(bot))