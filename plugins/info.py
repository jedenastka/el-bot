import discord

async def c_info_guild(ctx, guild=None):
    if guild is not None:
        try:
            tmp = ctx.bot.get_guild(int(guild))
        except:
            await ctx.message.channel.send(f"Can't find guild `{guild}`.")
            return
        else:
            guild = tmp
    else:
        guild = ctx.message.guild

    region = {
        discord.VoiceRegion.amsterdam: 'Amsterdam',
        discord.VoiceRegion.brazil: 'Brazil',
        discord.VoiceRegion.dubai: 'Dubai',
        discord.VoiceRegion.eu_central: 'Europe (Central)',
        discord.VoiceRegion.eu_west: 'Europe (West)',
        discord.VoiceRegion.europe: 'Europe',
        discord.VoiceRegion.frankfurt: 'Frankfurt',
        discord.VoiceRegion.hongkong: 'Hong Kong',
        discord.VoiceRegion.india: 'India',
        discord.VoiceRegion.japan: 'Japan',
        discord.VoiceRegion.london: 'London',
        discord.VoiceRegion.russia: 'Russia',
        discord.VoiceRegion.singapore: 'Singapore',
        discord.VoiceRegion.southafrica: 'South Africa',
        discord.VoiceRegion.sydney: 'Sydney',
        discord.VoiceRegion.us_central: 'United States (Central)',
        discord.VoiceRegion.us_east: 'United States (East)',
        discord.VoiceRegion.us_south: 'United States (South)',
        discord.VoiceRegion.us_west: 'United States (West)',
        discord.VoiceRegion.vip_amsterdam: 'Amsterdam (VIP)',
        discord.VoiceRegion.vip_us_east: 'United States (East, VIP)',
        discord.VoiceRegion.vip_us_west: 'United States (West, VIP)'
    }

    embed = discord.Embed(
        title=guild.name,
        description=f"""**Created:** {guild.created_at.strftime(r'%d.%m.%Y %H:%M:%S.%f')}
        **Owner:** {guild.owner.mention}
        **ID:** {guild.id}
        **Region:** {region.get(guild.region, str(guild.region))}
        **Member count:** {guild.member_count}
        **Channel count:** Text - {len(guild.text_channels)}, Voice - {len(guild.voice_channels)}, Categories - {len(guild.categories)}, Total - {len(guild.channels)}
        **Role count:** {len(guild.roles)}
        **Emoji count:** {len(guild.emojis)}
        **Boost count:** {guild.premium_subscription_count}"""
    )
    embed.set_thumbnail(url = guild.icon_url)
    await ctx.message.channel.send(embed=embed)

async def c_info_user(ctx, user=None):
    user = ctx.message.author
    try:
        user = int(user)
        guild = ctx.bot.get_guild(guildID)
        if guild is None:
            raise
    except:
        await ctx.message.channel.send(f"Can't find guild `{guildID}`.")
        return

async def c_info_message(ctx, message):
    pass

async def c_info_channel(ctx, channel=None):
    pass

events = [
    {
        'type': 'command',
        'name': 'info',
        'aliases': [],
        'callable': None,
        'subcommands': [
            {
                'type': 'command',
                'name': 'guild',
                'aliases': ['server'],
                'callable': c_info_guild
            },
            {
                'type': 'command',
                'name': 'user',
                'aliases': [],
                'callable': c_info_user
            },
            {
                'type': 'command',
                'name': 'message',
                'aliases': [],
                'callable': c_info_message
            },
            {
                'type': 'command',
                'name': 'channel',
                'aliases': [],
                'callable': c_info_channel
            }
        ]
    }
]