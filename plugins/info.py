import discord
from discord.ext import commands

"""
Name: info
Description: El Bot plugin for information about things.
Author: Grzesiek11
Version: v1.0.0
"""

class InfoPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Information commands
    @commands.group(name = 'info', aliases = ['information'])
    async def _info(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    # Server info
    @_info.command(name = 'server', aliases = ['guild'])
    async def _server(self, ctx):
        server = ctx.message.guild
        textChannels = ''
        for channel in server.text_channels:
            textChannels += channel.name + ', '
        textChannels = textChannels[:-2]
        voiceChannels = ''
        for channel in server.voice_channels:
            voiceChannels += channel.name + ', '
        voiceChannels = voiceChannels[:-2]
        emojis = ''
        for emoji in server.emojis:
            emojis += str(emoji) + ' '
        serverInfoEmbed = discord.Embed(title = server.name)
        serverInfoEmbed.description = f'''**Server info:**

        **ID:** {server.id}
        **Region:** {server.region}
        **Owner:** {server.owner}
        **User count:** {server.member_count}
        **Created at:** {server.created_at}
        **Channel count:** *Text* - {len(server.text_channels)}, *Voice* - {len(server.voice_channels)}, *All* - {len(server.text_channels) + len(server.voice_channels)}
        **Channels:** *Text* - {textChannels}, *Voice* - {voiceChannels}
        **Emojis:** {emojis} ({len(server.emojis)})'''
        await ctx.send(embed = serverInfoEmbed)

    # User info
    @_info.command(name = 'user', aliases = ['member'])
    async def _user(self, ctx, user : discord.Member = None):
        if user == None:
            user = ctx.author
        roles = ''
        for role in user.roles:
            roles += role.mention + ', '
        roles = roles[:-2]
        userInfoEmbed = discord.Embed(title = user.name, color = user.colour)
        userInfoEmbed.set_thumbnail(url = user.avatar_url)
        if user.activity != None:
            activity = user.activity.name
        else:
            activity = None
        userInfoEmbed.description = f'''**User info:**
        
        **Server nickname:** {user.nick}
        **ID:** {user.id}
        **Status:** {user.status}
        **Activity:** {activity}
        **Registered at:** {user.created_at}
        **Joined at:** {user.joined_at}
        **Is bot:** {user.bot}
        **Color:** {user.colour}
        **Roles:** {roles}
        **Top role:** {user.top_role.mention}'''
        await ctx.send(embed = userInfoEmbed)

def setup(bot):
    bot.add_cog(InfoPlugin(bot))