import discord
from discord.ext import commands
from gtts import gTTS as gtts
import os

"""
Name: tts
Description: El Bot plugin for TTS on VC.
Author: Grzesiek11
Version: v1.0.2
"""

os.makedirs('cache/tts', exist_ok=True)

class TTSPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name = 'tts')
    async def _tts(self, ctx):
        if ctx.invoked_subcommand is None:
            return
    
    @_tts.command(name = 'join', aliases = ['connect', 'c'])
    async def _join(self, ctx, channel : discord.VoiceChannel):
        await channel.connect()

    @_tts.command(name = 'say')
    async def _say(self, ctx, text, lang = 'en'):
        message = gtts(text, lang = lang)
        message.save('cache/tts/tts.mp3')
        ctx.guild.voice_client.play(discord.FFmpegPCMAudio('cache/tts/tts.mp3'))

    @_tts.command(name = 'disconnect', aliases = ['dc'])
    async def _disconnect(self, ctx):
        await ctx.guild.voice_client.disconnect()

def setup(bot):
    bot.add_cog(TTSPlugin(bot))