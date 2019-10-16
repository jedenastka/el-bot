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

    @commands.command(name = 'fortune')
    async def _fortune(self, ctx):
        while True:
            cookie = os.popen("fortune").read()
            if len(cookie) < 2000:
                break
        await ctx.send(cookie)
    
def setup(bot):
    bot.add_cog(UtilPlugin(bot))