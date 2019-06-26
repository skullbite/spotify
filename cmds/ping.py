import discord
import time
def setup(bot):
    @bot.command()
    async def ping(ctx):
        """Yes i'm alive."""
        em = discord.Embed(description="Please wait...", color=bot.color)
        em.set_author(name="Spotify", icon_url="https://cdn.discordapp.com/emojis/585861960613101573.gif?v=1")
        before = time.monotonic()
        msg = await ctx.send(embed=em)
        msgping = round((time.monotonic() - before) * 1000)
        em2 = discord.Embed(description=f"MSG: `{msgping}ms`\nAPI: `{round(bot.latency * 1000)}ms`", color=bot.color)
        await msg.edit(embed=em2)