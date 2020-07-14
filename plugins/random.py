import random

async def c_random(ctx, start, end):
    await ctx.message.channel.send(random.randrange(int(start), int(end)))

async def c_random_choice(ctx, *choices):
    await ctx.message.channel.send(random.choice(choices))

events = [
    {
        'type': 'command',
        'name': 'random',
        'alias': ['rand'],
        'callable': c_random,
        'subcommands': [
            {
                'type': 'command',
                'name': 'choice',
                'alias': ['ch'],
                'callable': c_random_choice,
                'subcommands': [
                    {
                        'type': 'command',
                        'name': 'test',
                        'alias': ['t'],
                        'callable': c_random_choice,
                        'subcommands': []
                    }
                ]
            }
        ]
    }
]