import sys
import re

import requests

import discord

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

    await ctx.send(embed=embed)

events = [
    {
        'type': 'command',
        'name': 'xkcd',
        'aliases': [],
        'callable': c_xkcd
    }
]