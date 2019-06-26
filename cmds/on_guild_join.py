import discord
import datetime
import json
import requests as req

config = json.load(open("config.json"))
def setup(bot):
   @bot.event
   async def on_guild_join(g):
       members = len([x for x in g.members if not x.bot])
       bots = len(g.members) - members
       uwu = req.post(f"https://discordbots.org/api/bots/{bot.user.id}/stats", headers={"Authorization": json.load(open("config.json"))["dbl"]}, data={"server_count": len(bot.guilds)}).json()
       bfd = req.post(f"https://botsfordiscord.com/api/bot/{bot.user.id}", headers={"Authorization": config["bfd"]}, data={"server_count": bot.guilds.__len__()}).json()
       em = discord.Embed(timestamp=datetime.datetime.utcnow(), color=0x36393f, description=f"▫Name: {g.name}\n▫Members to Bots: {members} to {bots}\n▫ID: {g.id}\n▫Owner: {g.owner}\n").set_author(name="New Guild", icon_url="https://cdn.discordapp.com/emojis/587878217902456832.png").set_footer(text=f"Now in {len(bot.guilds)} Guilds!").set_thumbnail(url=g.icon_url)
       await bot.doge.send(embed=em)
