import discord
import os
import psutil
import requests
import json
config = json.load(open("config.json"))

process = psutil.Process(os.getpid())
epic = requests.get("https://discordbots.org/api/bots/585225058683977750", headers={'Authorization': config.get("dbl")}).json()
def setup(bot):
    @bot.command()
    async def info(ctx):
        """Uninteresting things to know about me."""  
        skull = bot.get_user(158750488563679232)
        ramUsage = process.memory_full_info().rss / 1024**2
        em = discord.Embed(color=bot.color).set_author(name="Spotify Stats", icon_url=bot.img)
        em.title = "Here's a few unintersting things to know about me."
        em.description = f"▫Guilds: {len(bot.guilds)}\n▫Users: {len(bot.users)}\n▫[Votes](https://discordbots.org/bot/585225058683977750/vote): {epic['points']}\n▫RAM in use: {ramUsage:.2f}MB\n▫Commands used: {bot.stats['cmds_used']}"
        em.set_thumbnail(url=bot.user.avatar_url_as(format="png"))
        em.set_footer(text=f"Made by {skull}", icon_url=skull.avatar_url)
        await ctx.send(embed=em)
