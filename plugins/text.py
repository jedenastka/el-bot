async def c_say(ctx, *, text):
    await ctx.message.channel.send(text)

async def c_emotize(ctx, *, text):
    numbersInWords = {
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

    emotizedText = ''
    for ch in text:
        if ch.isalpha():
            emotizedText += f":regional_indicator_{ch}:"
        elif ch.digit():
            emotizedText += f":{int(ch)}:"
        elif ch in special.keys():
            emotizedText += special[ch]

    await ctx.message.channel.send(emotizedText)

async def c_space(ctx, *, text):
    spacedText = ''
    for ch in text:
        spacedText += ch + " "
    await ctx.message.channel.send(spacedText)

events = [
    {
        'type': 'command',
        'name': 'say',
        'aliases': [],
        'callable': c_say
    },
    {
        'type': 'command',
        'name': 'emotize',
        'aliases': ['big'],
        'callable': c_emotize
    },
    {
        'type': 'command',
        'name': 'space',
        'aliases': [],
        'callable': c_space
    }
]