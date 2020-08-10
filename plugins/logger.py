import datetime
import os

os.makedirs('fs/var/logger', exist_ok=True)

def log(text):
    print(text)
    with open('fs/var/logger/el.log', 'a') as logfile:
        logfile.write(f"{text}\n")

async def logMessages(ctx):
    log(f"[MESSAGE] [{datetime.datetime.now().strftime(r'%d.%m.%Y %H:%M:%S')}] [{ctx.message.channel.id} {ctx.message.author.id}] {ctx.message.content}")

async def logDeletes(ctx):
    log(f"[DELETION] [{datetime.datetime.now().strftime(r'%d.%m.%Y %H:%M:%S')}] [{ctx.message.channel.id} {ctx.message.author.id}] {ctx.message.content}")

async def logEdits(ctx, before, after):
    log(f"[EDIT] [{datetime.datetime.now().strftime(r'%d.%m.%Y %H:%M:%S')}] [{before.channel.id} {before.author.id}] {before.content} [CHANGED TO] {after.content}")

events = [
    {
        'type': 'onMessage',
        'callable': logMessages
    },
    {
        'type': 'onDelete',
        'callable': logDeletes
    },
    {
        'type': 'onEdit',
        'callable': logEdits
    }
]