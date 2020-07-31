import os

async def c_nmap(ctx):
    await ctx.message.channel.send(f"```\n{os.popen('nmap -p25565 91.231.24.247').read()}\n```")

events = [
    {
        'type': 'command',
        'name': 'nmap',
        'aliases': [],
        'callable': c_nmap
    }
]
