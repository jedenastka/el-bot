import discord
from discord.ext import commands

"""
Name: text
Description: El Bot plugin for formatting text.
Author: Grzesiek11
Version: v1.0.0
"""

class TextPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.group(name = 'text', aliases = ['txt'])
    async def _text(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    # Convert chars to big, emoticon chars
    @_text.command(name = 'emotize', aliases = ['big', 'emoticon'])
    async def _emotize(self, ctx, *, text : str):
        normalizeChars = {
            "ę" : "e",
            "ó" : "o",
            "ą" : "a",
            "ś" : "s",
            "ł" : "l",
            "ż" : "z",
            "ź" : "z",
            "ć" : "c",
            "ń" : "n"
        }
        numbersToWords = {
            0 : "zero",
            1 : "one",
            2 : "two",
            3 : "three",
            4 : "four",
            5 : "five",
            6 : "six",
            7 : "seven",
            8 : "eight",
            9 : "nine"
        }
        special = {
            ' ' : '        ',
            '!' : ':grey_exclamation:',
            '?' : ':grey_question:',
            '$' : ':heavy_dollar_sign:',
            '>' : ':arrow_forward:',
            '<' : ':arrow_backward:',
            '#' : ':hash:',
            '*' : ':asterisk:',
            '^' : ':arrow_up_small:'
        }
        text = text.lower()
        possible = " qwertyuiopasdfghjklzxcvbnm0123456789!?$<>#*^"
        final = ""
        for i in range(len(text)):
            # normalize polish characters
            text = text[0:i] + normalizeChars.get(text[i], text[i]) + text[i+1:len(text)]
            # test if st[i] is avalible character (from poss)
            if text[i] not in possible:
                continue
            # test is is or isn't numeric and add to final text
            if not text[i].isnumeric():
                if text[i] in special:
                    final += special.get(text[i])
                else:
                    final += ":regional_indicator_" + text[i] + ": "
            else:
                final += ":" + numbersToWords.get(int(text[i]), "zero") + ": "
        await ctx.send(final)

    # s p a c e  t h i s
    @_text.command(name = 'space')
    async def _space(self, ctx, *, text : str):
        textList = list(text)
        for i in range(len(textList)):
            textList.insert(i*2-1, " ")
        del textList[len(textList)-2]
        await ctx.send(''.join(textList))

    # Too many spoilers...
    @_text.command(name = 'spoilerize')
    async def _spoilerize(self, ctx, *, text : str):
        message = ""
        for i in text:
            message += f"||{i}||"
        await ctx.send(message)

    # Reply with same message
    @_text.command(name = 'say')
    async def _say(self, ctx, *, message : str):
        await ctx.send(message)

    # \n this
    @_text.command(name = 'enter', aliases = ['newline'])
    async def _enter(self, ctx, *, text : str):
        textTup = tuple(text)
        for i in textTup:
            if i == ' ':
                await ctx.send('_ _')
            else:
                await ctx.send(i)

def setup(bot):
    bot.add_cog(TextPlugin(bot))