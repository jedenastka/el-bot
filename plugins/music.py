import discord
from discord.ext import commands
import youtube_dl, os

"""
Name: music
Description: El Bot plugin for music.
Author: Grzesiek11
Version: v1.0.0
"""

os.makedirs('cache/music', exist_ok=True)


class MusicPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name = 'music', aliases = ['mus'])
    async def _music(self, ctx):
        if ctx.invoked_subcommand is None:
            return
    
    @_music.command(name = 'join', aliases = ['connect', 'c'])
    async def _join(self, ctx, channel : discord.VoiceChannel):
        await channel.connect()

    @_music.command(name = 'play', aliases = ['p'])
    async def _play(self, ctx, youtubeLink):
        youtube_dl.YoutubeDL({'format': 'bestaudio/best','outtmpl': 'cache/music/music.%(ext)s', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}).download([youtubeLink])
        ctx.guild.voice_client.originalSource = discord.FFmpegPCMAudio('cache/music/music.mp3')
        ctx.guild.voice_client.play(ctx.guild.voice_client.originalSource)

    @_music.command(name = 'disconnect', aliases = ['dc'])
    async def _disconnect(self, ctx):
        await ctx.guild.voice_client.disconnect()

    @_music.command(name = 'volume', aliases = ['vol'])
    async def _volume(self, ctx, percent : float):
        ctx.guild.voice_client.source = discord.PCMVolumeTransformer(ctx.guild.voice_client.originalSource, volume = percent / 100.0)

    @_music.command(name = 'pause')
    async def _pause(self, ctx):
        voiceClient = ctx.guild.voice_client
        if voiceClient.is_playing():
            voiceClient.pause()
        else:
            ctx.send('Nothing to pause.')
    
    @_music.command(name = 'resume')
    async def _resume(self, ctx):
        voiceClient = ctx.guild.voice_client
        if voiceClient.is_paused():
            voiceClient.resume()
        else:
            ctx.send('Nothing to resume.')
    
def setup(bot):
    bot.add_cog(MusicPlugin(bot))