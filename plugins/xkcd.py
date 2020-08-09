import sys
import re

import requests

import discord

viewers = {}

async def c_xkcd(ctx, comic='random'):
    if comic == 'random':
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
    viewers.update({message.id: int(comicId)})
    await message.add_reaction('\N{LEFTWARDS ARROW WITH HOOK}')
    await message.add_reaction('\N{LEFTWARDS BLACK ARROW}')
    await message.add_reaction('\N{TWISTED RIGHTWARDS ARROWS}')
    await message.add_reaction('\N{BLACK RIGHTWARDS ARROW}')
    await message.add_reaction('\N{RIGHTWARDS ARROW WITH HOOK}')

async def viewerInteraction(ctx, reaction, user):
    if user.id == ctx.bot.user.id:
        return
    comicId = viewers.get(reaction.message.id)
    if comicId is None:
        return
    
    if reaction.emoji == '\N{LEFTWARDS ARROW WITH HOOK}':
        comicId = 1
    elif reaction.emoji == '\N{LEFTWARDS BLACK ARROW}':
        comicId -= 1
    elif reaction.emoji == '\N{TWISTED RIGHTWARDS ARROWS}':
        r = requests.get('https://c.xkcd.com/random/comic/')
        comicId = re.search('https:\/\/xkcd.com\/(\d+)\/', r.url).group(1)
    elif reaction.emoji == '\N{BLACK RIGHTWARDS ARROW}':
        comicId += 1
    elif reaction.emoji == '\N{RIGHTWARDS ARROW WITH HOOK}':
        r = requests.get('https://xkcd.com/info.0.json')
        comicId = r.json()['num']
    else:
        await reaction.remove(user)
        return
    
    r = requests.get(f"https://xkcd.com/{comicId}/info.0.json")
    if r.status_code != 200:
        await reaction.remove(user)
        return
    response = r.json()

    embed = discord.Embed(
        title=f"{comicId} - {response['safe_title']}"
    )
    embed.set_image(url=response['img'])
    embed.set_author(name='xkcd.com', url=f"https://xkcd.com/{comicId}/", icon_url='https://grzesiek11.stary.pc.pl/el/xkcd2.png')
    embed.set_footer(text=response['alt'])

    await reaction.message.edit(embed=embed)
    viewers.update({reaction.message.id: int(comicId)})
    await reaction.remove(user)

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