import discord
def setup(bot):
    bot.remove_command('help')
    @bot.command()
    async def help(ctx):
        commands = [f"`{x.name}`" for x in bot.commands if not x.hidden]
        locked = [f"`{x.name}`" for x in bot.commands if x.checks != [] and x.checks[0].__qualname__ == "has_voted"]
        em = discord.Embed(color=bot.color, description=f"Prefixes: sp! or {bot.user.mention} | Spotify currently has {len(commands) + len(locked)} commands.").set_author(name="Spotify Help", icon_url=bot.img).add_field(name="Main Commands", value=" ".join(commands)).add_field(name="Music Commands", value=" ".join(locked))
        em.set_footer(text="Thank you for choosing spotify!")
        await ctx.send(embed=em)
