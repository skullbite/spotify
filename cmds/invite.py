import discord
def setup(bot):
    @bot.command(aliases=["add"])
    async def invite(ctx):
       em = discord.Embed(color=bot.color, description="You can add me by clicking [here](https://discordapp.com/oauth2/authorize?client_id=585225058683977750&scope=bot&permissions=18432).")
       em.set_author(name="Spotify", icon_url=bot.img)
       #em.set_footer(text="Thank you f")
       await ctx.send(embed=em)
