import spotify
from utils.d import dataIO as d
import discord
import random
def setup(bot):
    @bot.command()
    async def artist(ctx, *, artist: str):
        """Gets information on an artist."""
        em = discord.Embed(color=bot.color)
        results = await bot.spclient.search(artist)
        try:
            artist = results['artists'][0]
        except Exception as e:
            em.set_author(name="Sorry.", icon_url=bot.img)
            em.description = "No artist was found from your search."
            return await ctx.send(embed=em)
        extra_artists = []
        try:
            more = await artist.related_artists() 
        except:
            em.set_author(name="Sorry.", icon_url=bot.img)
            em.description = f"No artist was found from your search."
            
            return await ctx.send(embed=em)
        followers = "{:,}".format(artist.followers)
        all = await artist.total_albums()
        if more == []:
            extra_artists = ""
        else:
            for i in range(3):
                extra_artists.append(random.choice(more))
            extra_artists = f"▫Related Artists: " + ', '.join([f'[{x.name}](https://open.spotify.com/artist/{x.id})' for x in extra_artists])
            
        em.set_author(name=artist.name, icon_url=bot.img, url=f"https://open.spotify.com/artist/{artist.id}")
        try:
            em.set_thumbnail(url=artist.images[0]['url'])
        except:
            pass
        em.description = f"▫Tags: {', '.join(artist.genres)}\n" + f"▫Artist ID: {artist.id}\n" + f"▫Followers: {followers}\n" + f"▫Total Albums: {all}\n" + f"{extra_artists}\n" 

        await ctx.send(embed=em)

        
