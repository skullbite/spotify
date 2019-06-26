import discord
def setup(bot):
    @bot.command()
    async def vote(ctx):
        em = discord.Embed(color=bot.color, description="If you enjoy what I do, [voting](https://botsfordiscord.com/bot/585225058683977750/vote) would help other people notice. Also support further development.").set_author(name="Vote for Spotify", icon_url=bot.img).set_image(url="https://botsfordiscord.com/api/bot/585225058683977750/widget?theme=dark")
        await ctx.send(embed=em)
