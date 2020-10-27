import subprocess
import re

async def c_eval(ctx, *code):
    if ctx.message.author != (await ctx.bot.application_info()).owner:
        return
    
    code = ' '.join(code)

    m = re.fullmatch(r'```.*\n((.*\n)+)```', code)
    if m:
        code = m.group(1)
    
    exec(
        f'async def __ex(ctx): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )

    await locals()['__ex'](ctx)

async def c_sh(ctx, *command):
    if ctx.message.author != (await ctx.bot.application_info()).owner:
        return
    
    command = ' '.join(command)

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    await ctx.send(f"```\n{result.stdout.decode('UTF-8')}\n```")

events = [
    {
        'type': 'command',
        'name': 'eval',
        'aliases': [],
        'callable': c_eval
    },
    {
        'type': 'command',
        'name': 'sh',
        'aliases': [],
        'callable': c_sh
    }
]