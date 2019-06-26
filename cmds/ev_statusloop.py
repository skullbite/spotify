import discord
import asyncio
import random
def setup(bot):
    @bot.event
    async def statusloop():
        """loops playing status"""
        if not bot.is_ready():
            return
        playing = {'statuses': ["with metadata", f"with {len(bot.guilds)} servers", "with your playlist"], 'type': 0}
        listening = {'statuses': ["music without premium", "uwu by chevy", "whatever the guy next to you is listening to", "your secret playlist"], 'type': discord.ActivityType.listening}
        json = random.choice([playing, listening])
        await bot.change_presence(activity=discord.Game(random.choice(json.get("statuses")) + " | sp!help", type=json.get("type")))
        await asyncio.sleep(30)
        
    bot.loop.create_task(statusloop())
