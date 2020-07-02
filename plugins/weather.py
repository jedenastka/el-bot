import discord
from discord.ext import commands
from datetime import datetime

class WeatherPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'thunder')
    async def _thunder(self, ctx):
        await ctx.send(f"http://images.blitzortung.org/Images/image_b_pl.png?mapId={int(datetime.now().timestamp * 1000)}")
    
def setup(bot):
    bot.add_cog(WeatherPlugin(bot))