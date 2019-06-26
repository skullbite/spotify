from bot import Spotify
from discord.ext import commands
import os
from json import load
config = load(open("config.json"))
prefixes = ["sp!", "Sp!", "SP!", "sP!"]
bot = Spotify(command_prefix=commands.when_mentioned_or(*prefixes), shard_count=2)

for x in os.listdir("cmds"):
    if not x == "__pycache__":
        file = x[:-3]
        try:
            bot.load_extension(f"cmds.{file}")
        except Exception as e:
            print(f"[ERROR][{file}]: {e}")
            pass
    
bot.run(config["token"])
