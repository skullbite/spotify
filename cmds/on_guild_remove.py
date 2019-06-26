import discord
import datetime
def setup(bot):
   @bot.event
   async def on_guild_remove(g):
       em = discord.Embed(timestamp=datetime.datetime.utcnow(), color=0x36393f, description=f"▫Name: {g.name}\n▫ID: {g.id}\n▫Owner: {g.owner}").set_author(name="Guild Lost", icon_url="https://cdn.discordapp.com/emojis/587878411930828801.png").set_footer(text=f"Now in {len(bot.guilds)} Guilds.").set_thumbnail(url=g.icon_url)
       await bot.doge.send(embed=em)
