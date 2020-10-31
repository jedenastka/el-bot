import sys
import re

import discord

from botutils import getServerDoc, updateServerDoc, mergeDicts

import requests

dbPath = ['plugins', 'xkcd']

async def c_xkcd(ctx, *comic):
    comic = ' '.join(comic)

    if comic == 'random' or comic == '':
        r = requests.get('https://c.xkcd.com/random/comic/')
        comicId = re.search('https:\/\/xkcd.com\/(\d+)\/', r.url).group(1)
    elif comic == 'latest':
        r = requests.get('https://xkcd.com/info.0.json')
        comicId = r.json()['num']
    elif comic.isdigit():
        comicId = comic
    else:
        r = requests.get('https://xkcd.com/archive/')
        comics = re.findall('<a href="\/(\d+)\/" title="\d+-\d+-\d+">(.+?)<\/a><br\/>', r.text)

        comicId = None
        for potentialComic in comics:
            if potentialComic[1].lower().find(comic.lower()) != -1:
                comicId = potentialComic[0]
                break

        if comicId is None:
            await ctx.send(f"Can't find comic `{comic}`.")
            return

    r = requests.get(f"https://xkcd.com/{comicId}/info.0.json")
    response = r.json()

    embed = discord.Embed(
        title=f"{comicId} - {response['safe_title']}"
    )
    embed.set_image(url=response['img'])
    embed.set_author(name='xkcd.com', url=f"https://xkcd.com/{comicId}/", icon_url='https://grzesiek11.stary.pc.pl/el/xkcd2.png')
    embed.set_footer(text=response['alt'])

    message = await ctx.send(embed=embed)
    #viewers.update({message.id: {'id': int(comicId), 'user': ctx.message.author.id}})
    updateServerDoc(ctx.message.guild.id, {**getServerDoc(ctx.message.guild.id, dbPath + ['viewers']), str(message.id): {'id': int(comicId), 'user': ctx.message.author.id}}, dbPath + ['viewers'])
    await message.add_reaction('\N{LEFTWARDS ARROW WITH HOOK}')
    await message.add_reaction('\N{LEFTWARDS BLACK ARROW}')
    await message.add_reaction('\N{TWISTED RIGHTWARDS ARROWS}')
    await message.add_reaction('\N{BLACK RIGHTWARDS ARROW}')
    await message.add_reaction('\N{RIGHTWARDS ARROW WITH HOOK}')

async def viewerInteraction(ctx, emoji, user):
    if user.id == ctx.bot.user.id:
        return
    comic = getServerDoc(ctx.message.guild.id, dbPath + ['viewers', str(ctx.message.id)], addOverlay=True)
    if comic == {}:
        return
    
    if user.id != comic['user']:
        await ctx.message.remove_reaction(emoji, user)
        return

    if emoji == '\N{LEFTWARDS ARROW WITH HOOK}':
        comic['id'] = 1
    elif emoji == '\N{LEFTWARDS BLACK ARROW}':
        comic['id'] -= 1
    elif emoji == '\N{TWISTED RIGHTWARDS ARROWS}':
        r = requests.get('https://c.xkcd.com/random/comic/')
        comic['id'] = int(re.search('https:\/\/xkcd.com\/(\d+)\/', r.url).group(1))
    elif emoji == '\N{BLACK RIGHTWARDS ARROW}':
        comic['id'] += 1
    elif emoji == '\N{RIGHTWARDS ARROW WITH HOOK}':
        r = requests.get('https://xkcd.com/info.0.json')
        comic['id'] = r.json()['num']
    else:
        await ctx.message.remove_reaction(emoji, user)
        return
    
    r = requests.get(f"https://xkcd.com/{comic['id']}/info.0.json")
    if r.status_code != 200:
        await ctx.message.remove_reaction(emoji, user)
        return
    response = r.json()

    embed = discord.Embed(
        title=f"{comic['id']} - {response['safe_title']}"
    )
    embed.set_image(url=response['img'])
    embed.set_author(name='xkcd.com', url=f"https://xkcd.com/{comic['id']}/", icon_url='https://grzesiek11.stary.pc.pl/el/xkcd2.png')
    embed.set_footer(text=response['alt'])

    await ctx.message.edit(embed=embed)
    updateServerDoc(ctx.message.guild.id, comic, dbPath + ['viewers', str(ctx.message.id)])
    await ctx.message.remove_reaction(emoji, user)

events = [
    {
        'type': 'command',
        'name': 'xkcd',
        'aliases': [],
        'callable': c_xkcd
    },
    {
        'type': 'onReaction',
        'callable': viewerInteraction
    }
]