import datetime
import os

def logEvent(db, eventType: str, obj):
    if eventType == 'message':
        db['log'].insert_one({
            'type': 'message',
            'id': obj.id,
            'content': obj.content,
            'user': obj.author.id,
            'channel': obj.channel.id,
            'guild': obj.guild.id,
            'time': int(datetime.datetime.timestamp(obj.created_at))
        })
    elif eventType == 'edit':
        db['log'].insert_one({
            'type': 'edit',
            'id': obj[0].id,
            'content': obj[1].content,
            'time': int(datetime.datetime.timestamp(obj[1].edited_at))
        })
    elif eventType == 'delete':
        db['log'].insert_one({
            'type': 'delete',
            'id': obj.id,
            'time': int(datetime.datetime.now().timestamp())
        })

async def logMessages(ctx):
    logEvent(ctx.db, 'message', ctx.message)

async def logDeletes(ctx):
    logEvent(ctx.db, 'delete', ctx.message)

async def logEdits(ctx, before, after):
    logEvent(ctx.db, 'edit', (before, after))

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
            logEvent(ctx.db, 'message', message)
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