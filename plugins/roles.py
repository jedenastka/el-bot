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

async def reactionRoleAdd(ctx, emoji, user):
    reactionRoleMessages = getServerDoc(ctx.message.guild.id, dbPath + ['reactionRoles'])
    reactionRoles = reactionRoleMessages.get(str(ctx.message.id))

    if reactionRoles is None:
        return

    roleId = reactionRoles.get(str(emoji))
    
    if roleId is None:
        return

    await user.add_roles(ctx.message.guild.get_role(roleId))

async def reactionRoleRemove(ctx, emoji, user):
    reactionRoleMessages = getServerDoc(ctx.message.guild.id, dbPath + ['reactionRoles'])
    reactionRoles = reactionRoleMessages.get(str(ctx.message.id))

    if reactionRoles is None:
        return

    roleId = reactionRoles.get(str(emoji))
    
    if roleId is None:
        return

    await ctx.message.author.remove_roles(ctx.message.guild.get_role(roleId))

events = [
    {
        'type': 'command',
        'name': 'role',
        'aliases': [],
        'callable': c_role
    },
    {
        'type': 'onReaction',
        'callable': reactionRoleAdd
    },
    {
        'type': 'onReactionRemove',
        'callable': reactionRoleRemove
    }
]