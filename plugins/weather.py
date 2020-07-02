import discord
from discord.ext import commands
from datetime import datetime
import requests

class WeatherPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'thunder')
    async def _thunder(self, ctx):
        await ctx.send(f"http://images.blitzortung.org/Images/image_b_pl.png?mapId={int(datetime.now().timestamp() * 1000)}")

    @commands.command(name = 'weather')
    async def _weather(self, ctx, city: str):
        await ctx.send('```' + requests.get(f'http://wttr.in/{city}?0&T&q').text + '```')
    
def setup(bot):
    bot.add_cog(WeatherPlugin(bot))