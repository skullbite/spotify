import discord
from utils.checks import is_owner
from discord.ext import commands
def setup(bot):
    @bot.command()
    async def search(ctx, *, query: str):
        em = discord.Embed(color=bot.color)
        em.set_author(name="Search Results", icon_url=bot.img)
        res = await bot.spclient.search(query, limit=5)
        for key in res:
            var = res[key]
            if var == []:
                pass
            else:
                
                em.add_field(name=key.title(), value=", ".join([f"[{x.name}](https://open.spotify.com/{key[:-1]}/{x.id})" for x in var]))
        
        if len(em.fields) == 0:
            em.description = "No results found."
        await ctx.send(embed=em)
