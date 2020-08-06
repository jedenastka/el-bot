import random

async def c_random(ctx, start, stop):
    await ctx.send(random.randrange(int(start), int(stop)))

async def c_random_coin(ctx):
    await ctx.send(random.choice(('Heads!', 'Tails!')))

async def c_random_choice(ctx, *options):
    await ctx.send(random.choice(options))

events = [
    {
        'type': 'command',
        'name': 'random',
        'aliases': ['rand'],
        'callable': c_random,
        'subcommands': [
            {
                'type': 'command',
                'name': 'coin',
                'aliases': ['flip'],
                'callable': c_random_coin
            },
            {
                'type': 'command',
                'name': 'choose',
                'aliases': ['choice'],
                'callable': c_random_choice
            }
        ]
    }
]