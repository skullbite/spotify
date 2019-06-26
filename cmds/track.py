import discord
from utils.d import dataIO as d
import lavalink
def setup(bot):
    @bot.command()
    async def track(ctx, *, track: str):
        """Gets info on a track"""
        em = discord.Embed(color=bot.color)
        res = await bot.spclient.search(track)
        try:
            track = res['tracks'][0]
        except Exception as e:
            em.set_author(name="Sorry.", icon_url=bot.img)
            em.description = "No track was found for your search."
            #em.description = e
            return await ctx.send(embed=em)
        
        em.set_author(name=track.name, icon_url=bot.img, url=f"https://open.spotify.com/track/{track.id}")
        em.set_thumbnail(url=track._Track__data['album']['images'][0]['url'])
        em.description = f"▫Album: {track._Track__data['album']['name']}\n▫Released at {track._Track__data['album']['release_date']}\n" + f"▫Artist(s): {', '.join([x.name for x in track.artists])}\n" + f"▫Duration: {str(lavalink.Utils.format_time(track.duration))[3:]}\n▫Popularity: {track._Track__data['popularity']}%\n" + ("<:explicit:585821110210265092> This song is explicit." if track.explicit else "")
       
        await ctx.send(embed=em)
