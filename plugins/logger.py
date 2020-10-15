import datetime
import os

#os.makedirs('fs/var/logger', exist_ok=True)

#def log(text):
#    print(text)
#    with open('fs/var/logger/el.log', 'a') as logfile:
#        logfile.write(f"{text}\n")

def logEvent(eventType: str, obj):
    print(obj)
    if eventType == 'message':
        ctx.db['log'].insert_one({
            'type': 'message',
            'content': obj.content,
            'user': obj.author.id,
            'channel': obj.channel.id,
            'guild': obj.guild.id,
            'time': int(datetime.datetime.timestamp(obj.created_at))
        })
    elif eventType == 'edit':
        ctx.db['log'].insert_one({
            'type': 'edit',
            'id': obj[0].id,
            'content': obj[1].content,
            'time': int(datetime.datetime.timestamp(obj[1].edited_at))
        })
    elif eventType == 'delete':
        ctx.db['log'].insert_one({
            'type': 'delete',
            'id': obj.id,
            'time': int(datetime.datetime.now().timestamp())
        })

async def logMessages(ctx):
    logEvent('message', ctx.message)
    #log(f"[MESSAGE] [{datetime.datetime.now().strftime(r'%d.%m.%Y %H:%M:%S')}] [{ctx.message.channel.id} {ctx.message.author.id}] {ctx.message.content}")

async def logDeletes(ctx):
    logEvent('delete', ctx.message)
    #log(f"[DELETION] [{datetime.datetime.now().strftime(r'%d.%m.%Y %H:%M:%S')}] [{ctx.message.channel.id} {ctx.message.author.id}] {ctx.message.content}")

async def logEdits(ctx, before, after):
    logEvent('edit', (before, after))
    #log(f"[EDIT] [{datetime.datetime.now().strftime(r'%d.%m.%Y %H:%M:%S')}] [{before.channel.id} {before.author.id}] {before.content} [CHANGED TO] {after.content}")

async def c_scan(ctx):
    status = ["Initializing..."]
    statusMsg = await ctx.send('...')

    async def updateStatus():
        await statusMsg.edit(content='```\n' + '\n'.join(status) + '\n```')

    for channel in ctx.message.guild.text_channels:
        status.append(f"Scanning channel `{channel.name}`...")
        await updateStatus()

        i = 1
        async for message in channel.history(limit=None):
            ctx.db['log'].insert_one({
                'type': 'message',
                'message': message.content,
                'user': message.author.id,
                'channel': message.channel.id,
                'guild': message.guild.id,
                'time': int(datetime.datetime.timestamp(message.created_at))
            })
            if i % 500 == 0:
                status[len(status) - 1] = f"Scanning channel `{channel.name}` ({i} messages so far)..."
                await updateStatus()
            i += 1
        
        status[len(status) - 1] = f"Done scanning channel `{channel.name}`, scanned {i} messages."
        await updateStatus()

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
    },
    {
        'type': 'command',
        'name': 'scan',
        'aliases': [],
        'callable': c_scan
    }
]