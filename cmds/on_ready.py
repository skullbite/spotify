import discord
import aiohttp
import datetime
from json import load
config = load(open("config.json"))
def setup(bot):
    @bot.event
    async def on_ready():
        meh = discord.Embed(description="", color=0x36393f, timestamp=datetime.datetime.utcnow()).set_image(url="https://cdn.owopup.me/meme/doge.jpg").set_author(name="Ready", icon_url="https://cdn.discordapp.com/emojis/588403022481195028.png")
        if not hasattr(bot, 'doge'):
            session = aiohttp.ClientSession()
            bot.doge = discord.Webhook.from_url(config["webhook"], adapter=discord.AsyncWebhookAdapter(session))
        print(f"Ready: {bot.user} | Guilds: {len(bot.guilds)}")
        await bot.doge.send(embed=meh)
        await bot.change_presence(activity=discord.Game(name="sp!help"))
        
