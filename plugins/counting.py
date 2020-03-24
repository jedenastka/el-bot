import discord
from discord.ext import commands

"""
Name: counting
Description:
Author: Grzesiek11
Version: v1.0.0
"""

last = None
lastAuthor = None

class UtilPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        global last, lastAuthor
        delete = False
        if message.channel.id == 691341640903688262 and message.author != self.bot.user:
            if message.content.isdigit():
                digit = int(message.content)
                if last != None:
                    if last + 1 != digit or message.author == lastAuthor:
                        delete = True
            else:
                delete = True
        if delete:
            await message.delete()
        else:
            last = digit
            lastAuthor = message.author

def setup(bot):
    bot.add_cog(UtilPlugin(bot))
