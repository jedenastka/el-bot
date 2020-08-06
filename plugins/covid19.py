import requests

import discord

async def c_covid(ctx, country=None):
    embed = discord.Embed()

    if country is None:        
        r = requests.get('https://api.covid19api.com/world/total')
        response = r.json()

        embed.title = 'COVID-19 worldwide'

        confirmed = response['TotalConfirmed']
        died = response['TotalDeaths']
        recovered = response['TotalRecovered']
        active = confirmed - died - recovered
    else:
        r = requests.get(f"https://api.covid19api.com/total/country/{country}")
        response = r.json()

        try:
            if response['message'] == 'Not Found':
                await ctx.send(f"Country `{country}` not found.")
                return
            elif response['message'] is not None:
                await ctx.send(f"Unknown error ({response['message']}).")
                return
        except:
            pass
        
        response = response[-1]

        embed.title = f"COVID-19 in {response['Country']}"

        confirmed = response['Confirmed']
        died = response['Deaths']
        recovered = response['Recovered']
        active = response['Active']
    
    embed.description = f"""**Confirmed:** {'{0:,}'.format(confirmed).replace(',', ' ')}
    **Deaths:** {'{0:,}'.format(died).replace(',', ' ')}
    **Recovered:** {'{0:,}'.format(recovered).replace(',', ' ')}
    **Active:** {'{0:,}'.format(active).replace(',', ' ')}"""
    await ctx.send(embed=embed)

events = [
    {
        'type': 'command',
        'name': 'covid19',
        'aliases': ['c19', 'covid'],
        'callable': c_covid
    }
]