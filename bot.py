from discord.ext.commands import AutoShardedBot
import spotify
from collections import Counter
import json
config = json.load(open("config.json"))
class Spotify(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.spclient = spotify.Client(config["client_id"], config["client_secret"])
        self.color = 0x1ed760
        self.stats = Counter()
        self.img = "https://cdn.discordapp.com/emojis/382423939680305153.png"
        self.last = None
    
        


    



