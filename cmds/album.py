import discord
from utils.d import dataIO as d
def setup(bot):
    @bot.command()
    async def album(ctx, *, album: str):
        """Gets stats on an album."""
        em = discord.Embed(color=bot.color)
        results = await bot.spclient.search(album)
        try:
            album = results['albums'][0]
        except:
            em.set_author(name="Sorry.", icon_url=bot.img)
            em.description = "No artist was found from your search."
            return await ctx.send(embed=em)
        tracks = await album.total_tracks()
        em.set_author(name=f"{album.name} {('(Single)' if album.album_type == 'single' else '')}", icon_url=bot.img, url="")
        em.description = f"▫Released at {album.release_date}\n" + f"▫Artists: {', '.join([x.name for x in album.artists])}\n" + f"▫Total Tracks: {tracks}\n" #+ f"Genre: {album.genre}" 
        await ctx.send(embed=em)
        
