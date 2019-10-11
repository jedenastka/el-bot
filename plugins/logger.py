import discord
from discord.ext import commands
import json, time, datetime

"""
Name: logger
Description: El Bot plugin for logging messages, reactions, edits etc.
Author: Grzesiek11
Version: v1.0.0
"""

def appendToLog(self, fragment):
    log = open(self.bot.data["logfile"], 'a')
    log.write(fragment + '\n')
    log.close()

class LoggerPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Message logging
    @commands.Cog.listener()
    async def on_message(self, message):
        """fragment = {
            'type': 'message',
            'time': int(time.time()),
            'message': {
                'content': message.content,
                'id': message.id,
                'sendTime': message.created_at
            },
            'author': {
                'name': message.author.name,
                'id': message.author.id,
                'nick': message.author.nick,
                'registered': message.author.created_at,
                'joined': message.author.joined_at,
                'avatar': message.author.avatar_url_as(static_format = 'png'),
                'roles': message.author.roles,
                'status': message.author.status,
                'isBot': message.author.bot,
                'colour': message.author.colour
            },
            'server': {
                'name': message.guild.name,
                'id': message.guild.id,
                'owner': message.guild.owner,
                'createdAt': message.guild.created_at,
                'channels': message.guild.channels,
                'memberCount': message.guild.member_count
            },
            'channel': {
                'name': message.channel.name,
                'id': message.channel.id,
                'category': {
                    'name': message.channel.category.name,
                    'id': message.channel.category.id
                }
            }
        }
        print(fragment)"""
        appendToLog(self, f'''[{message.author}|{message.guild}|{message.channel}|{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}] {message.content}''')

def setup(bot):
    bot.add_cog(LoggerPlugin(bot))