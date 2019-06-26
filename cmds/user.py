import discord
import lavalink
from discord.ext import commands
def setup(bot):
    @bot.command()
    @commands.guild_only()
    async def user(ctx, *, user: discord.Member=None):
        """Gets info on a track somebody's listening to"""
        if not user:
           user = ctx.author
        em = discord.Embed(color=bot.color)
        try:    
            res = await bot.spclient.get_track(user.activity.track_id)
        
            track = res
        except Exception as e:
            em.set_author(name="Sorry.", icon_url=bot.img)
            if user == ctx.author:
                you = "You aren't "
            else:
                you = "This user isn't "
            em.description = f"{you}listening to spotify."
            #em.description = e
            return await ctx.send(embed=em)
        
        em.set_author(name=track.name, icon_url=bot.img, url=f"https://open.spotify.com/track/{track.id}")
        em.set_thumbnail(url=track._Track__data['album']['images'][0]['url'])
        owouwu = [f"[{x.name}](https://open.spotify.com/artist/{x.id})" for x in track.artists]
        em.description = f"▫Album: {track._Track__data['album']['name']}\n▫Released at {track._Track__data['album']['release_date']}\n" + f"▫Artist(s): {', '.join([x.name for x in track.artists])}\n" + f"▫Duration: {str(lavalink.Utils.format_time(track.duration))[3:]}\n▫Popularity: {track._Track__data['popularity']}%\n" + ("<:explicit:585821110210265092> This song is explicit." if track.explicit else "")
        em.set_footer(text=f"Listener: {user}", icon_url=user.avatar_url)
        #print(len(str(track._Track__data)) + track.href)
        await ctx.send(embed=em)
