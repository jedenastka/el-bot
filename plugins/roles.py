from botutils import getServerDoc

dbPath = ['plugins', 'roles']

async def c_role(ctx, *none):
    selfRoles = getServerDoc(ctx.message.guild.id, dbPath + ['selfRoles'])

    for role in ctx.message.role_mentions:
        if role.id in selfRoles:
            if role not in ctx.message.author.roles:
                await ctx.message.author.add_roles(role)
            else:
                await ctx.message.author.remove_roles(role)

events = [
    {
        'type': 'command',
        'name': 'role',
        'aliases': [],
        'callable': c_role
    }
]