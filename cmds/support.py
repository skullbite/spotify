import discord
import time
def setup(bot):
    @bot.command()
    async def support(ctx):
        """Ask for help"""
        em = discord.Embed(description="If you're having any issues please join [this server](https://discord.gg/c4vWDdd) and ask for help.", color=bot.color)
        em.set_author(name="Spotify", icon_url=bot.img)
        
        msg = await ctx.send(embed=em)
        