import discord
from discord.ext import commands

"""
Name: poll
Description: El Bot plugin for making polls.
Author: Grzesiek11
Version: v1.0.0
"""

class PollPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # Make a poll
    @commands.command(name = 'poll')
    async def _poll(self, ctx, topic : str, *answers : str):
        # dict to convert numbers to emoji
        numberEmoji = {
            0 : 'zero',
            1 : 'one',
            2 : 'two',
            3 : 'three',
            4 : 'four',
            5 : 'five',
            6 : 'six',
            7 : 'seven',
            8 : 'eight',
            9 : 'nine',
            10 : 'keycap_ten'
        }
        # get amount of answers
        answerAmount = len(answers)
        # check lenght
        if answerAmount > 11:
            answerAmount = 11
        elif answerAmount < 2:
            await ctx.send('Too few answers! You must give at least two.')
            return
        # add answers with number emojis to answersStr
        answersStr = ''
        for i in range(answerAmount):
            answersStr += f':{numberEmoji[i]}: {answers[i]}\n'
        # make and send embed
        pollEmbed = discord.Embed(
            title = f':clipboard: Poll - {topic}',
            description = answersStr
        )
        pollMsg = await ctx.send(embed = pollEmbed)
        # dict to convert numbers to reactions
        reactNumbers = {
            0 : '\N{DIGIT ZERO}',
            1 : '\N{DIGIT ONE}',
            2 : '\N{DIGIT TWO}',
            3 : '\N{DIGIT THREE}',
            4 : '\N{DIGIT FOUR}',
            5 : '\N{DIGIT FIVE}',
            6 : '\N{DIGIT SIX}',
            7 : '\N{DIGIT SEVEN}',
            8 : '\N{DIGIT EIGHT}',
            9 : '\N{DIGIT NINE}',
            10 : '\N{KEYCAP TEN}'
        }
        for i in range(answerAmount):
            react = reactNumbers[i]
            # add second part to reactions, 10 is special (it doesn't need this)
            if i != 10:
                react += '\N{COMBINING ENCLOSING KEYCAP}'
            await pollMsg.add_reaction(react)

    # Small poll (yes/no reaction-only)
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('+poll'):
            reacts = ['\N{THUMBS UP SIGN}', '\N{SHRUG}', '\N{THUMBS DOWN SIGN}']
            for react in reacts:
                await message.add_reaction(react)

def setup(bot):
    bot.add_cog(PollPlugin(bot))