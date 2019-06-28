"""https://github.com/EvieePy/Wavelink"""
import lavalink
import asyncio
import datetime
import discord
import humanize
import itertools
import re
import sys
import traceback
import wavelink
from discord.ext import commands
from typing import Union
from colorthief import ColorThief
from io import BytesIO
import requests
import spotify
from utils.checks import *
impprt json



RURL = re.compile('https?:\/\/(?:www\.)?.+')
config = json.load(open("config.json"))
class Track(wavelink.Track):
    __slots__ = ('requester', 'channel', 'message', 'strack')

    def __init__(self, id_, info, *, ctx=None, strack: spotify.Track):
        super(Track, self).__init__(id_, info)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.message = ctx.message
        self.strack = strack

class MusicController:
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None

        self.last = None
        self.loop = False
        self.next = asyncio.Event()
        self.queue = asyncio.Queue()

        self.volume = 50
        self.now_playing = None
        self.strack = None

        self.bot.loop.create_task(self.controller_loop())

    async def controller_loop(self):
        await self.bot.wait_until_ready()

        player = self.bot.wavelink.get_player(self.guild_id)
        await player.set_volume(self.volume)

        while True:
            
            try:
                await self.now_playing.delete()
            except:
                pass

            c = self.bot.get_channel(player.channel_id)
            if not c and not self.now_playing:
            	
                return await self.channel.send("I'm not in a voice channel. Please use `sp!connect`")
                
            #if len([x for x in c.members if not x.bot]) == 0:
            #    await self.bot.channel.send('Nobody was listening so I stopped playing.')
            #    del self.controllers[ctx.guild.id]
                #return await player.disconnect()


            #print(self.bot.get_channel(player.channel_id))
            if self.loop:
            	song = self.last
            else:
                song = await self.queue.get()
            self.next.clear()
            hhh = song.strack
            time = lavalink.Utils.format_time(int(song.length))
            img = BytesIO(requests.get(hhh._Track__data['album']['images'][0]['url']).content)
            color = ColorThief(img).get_color(quality=10)
            if time.startswith("00:"):
            	time = time[3:]
            em = discord.Embed(description=f"[{hhh.name}](https://open.spotify.com/track/{hhh.id}) | **`[{time}]`**", color=self.bot.color).set_thumbnail(url=hhh._Track__data['album']['images'][0]['url']).set_author(name="Now Playing", icon_url=self.bot.img).set_footer(text=f"Requested by {song.requester}", icon_url=song.requester.avatar_url)
            em.timestamp = song.message.created_at
            em.color = discord.Color.from_rgb(*color)
            await player.play(song)
            self.now_playing = await self.channel.send(embed=em)

            await self.next.wait()

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.em = None
        self.controllers = {}

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(self.bot)

        self.bot.loop.create_task(self.start_nodes())

    def cog_unload(self):
        for id in self.controllers:
            #del self.controllers[id]

            #player = self.bot.wavelink.get_player(id)
            #await player.disconnect()
            self.bot.wavelink.nodes.clear()

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        

        host = config["host"]
        port = config["port"]
        password = config["password"]
        for shard in list(self.bot.shards)
            node = await self.bot.wavelink.initiate_node(host=host,
                                                         port=port,
                                                         rest_uri=f'http://{host}:{port}',
                                                         shard_id=int(shard),
                                                         password=password,
                                                         identifier=f'Spotify Music. [{shard}]',
                                                         region='us_central')

            # Set our node hook callback
            node.set_hook(self.on_event_hook)

    async def on_event_hook(self, event):
        """Node hook callback."""
        if isinstance(event, (wavelink.TrackEnd, wavelink.TrackException)):
            controller = self.get_controller(event.player)
            controller.next.set()

    def get_controller(self, value: Union[commands.Context, wavelink.Player]):
        if isinstance(value, commands.Context):
            gid = value.guild.id
        else:
            gid = value.guild_id

        try:
            controller = self.controllers[gid]
        except KeyError:
            controller = MusicController(self.bot, gid)
            self.controllers[gid] = controller

        return controller

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, commands.CheckFailure):
        	return await ctx.send("Music is currently in testing. Thank You for your paticence.")
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        
    def build_search(track: spotify.Track):
    	return f"{track.name} {' '.join([x.name for x in track.artists])} audio"
    @commands.command(name='connect', aliases=['c'], hidden=True)
    @commands.check(has_voted)
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to a valid voice channel."""
        
        em = discord.Embed()
        
        if not channel:
            try:
                channel = ctx.author.voice.channel
                
            except AttributeError:
                em.description = 'You aren\'t in a voice channel. Please either specify a valid channel or join one.'
                em.color = self.bot.color
                return await ctx.send(embed=em)
      
        player = self.bot.wavelink.get_player(ctx.guild.id)
        em.description = f'Connected to **`{channel.name}`**'
        em.color = self.bot.color
        await ctx.send(embed=em, delete_after=15)
        try:
            await player.connect(channel.id)
        except:
        	pass
        await self.bot.shards[ctx.guild.shard_id].ws.voice_state(str(ctx.guild.id), channel.id)
        controller = self.get_controller(ctx)
        controller.channel = ctx.channel


    @commands.command(aliases=['p'], hidden=True)
    @commands.check(has_voted)
    async def play(self, ctx, *, query: str):
        """Search for and add a song to the Queue."""
        em = discord.Embed(color=self.bot.color)

        
        precheck = await self.bot.spclient.search(query)
        precheck = precheck["tracks"]
       
        if precheck == []:
        	return await ctx.send("No tracks were found.")
        track = precheck[0]
        search = f"{track.name} {' '.join([x.name for x in track.artists])} audio"
        
        tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{search}")


        if not tracks:
            return await ctx.send("No tracks were found.")
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send("I'm not in a voice channel. Please use `sp!connect`")
        if ctx.author.voice:
    	    if ctx.guild.me.voice.channel.id != ctx.author.voice.channel.id:
    	        return await ctx.send("Join my voice channel first.")
        else:
            return await ctx.send("Join my voice channel first.")
            "uwu"
        controller = self.get_controller(ctx)
        controller.channel = ctx.channel
  #      if isinstance(tracks, wavelink.TrackPlaylist):
#            for t in tracks.tracks:
#                await controller.queue.put(Track(t.id, t.info, ctx=ctx))

#            await ctx.send(f"Added `[{len(tracks.tracks)}]` Songs")
        
        track = tracks[0]
        strack = precheck[0]
        img = BytesIO(requests.get(strack._Track__data['album']['images'][0]['url']).content)
        color = ColorThief(img).get_color(quality=10)
        await controller.queue.put(Track(track.id, track.info, strack=strack, ctx=ctx))
        em.set_author(name="Track Enqueued.", icon_url=self.bot.img, url=f"https://open.spotify.com/track/{strack.id}")
        em.set_thumbnail(url=strack._Track__data['album']['images'][0]['url'])
        em.description = f"{strack.name} by {', '.join([x.name for x in strack.artists])}"
        em.color = discord.Color.from_rgb(*color)
        if list(controller.queue._queue) == [] and not player.current:
            return
        
        await ctx.send(embed=em, delete_after=15)

    @commands.command(hidden=True)
    @commands.check(has_voted)
    async def pause(self, ctx):
        """Pause the player."""
        em = discord.Embed(color=self.bot.color)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_playing:
            em.description = 'I am not currently playing anything.'
        
        em.description = 'The player is now paused.'
        await ctx.send(embed=em, delete_after=15)
        await player.set_pause(True)
      
#    @commands.command(hidden=True)
#    async def loop(self, ctx):
#    	"""Loops the current song."""
#    	player = self.bot.wavelink.get_player(ctx.guild.id)
#    	if not player.loop:
#    		player.loop = True
#    		return await ctx.send("Player is now looped.")
#    	
#    	player.loop = False
#    	await ctx.send("Player is no longer looped.")
    
    @commands.command(hidden=True)
    async def resume(self, ctx):
        """Resume the player from a paused state."""
        em = discord.Embed(color=self.bot.color)
        
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.paused:
           em.description = 'The player is not currently paused. Use `sp!pause` to pause it.'

        em.description = 'The layer is now resumed'
        await ctx.send(embed=em)
        await player.set_pause(False)

    @commands.command(hidden=True)
    @commands.check(has_voted)
    async def skip(self, ctx):
        """Skip the currently playing song."""
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('I am not currently playing anything.', delete_after=15)

        await ctx.send(f'{player.current.strack.name} has been skipped.', delete_after=15)
        await player.stop()

    @commands.command(hidden=True)
    @commands.check(has_voted)
    async def volume(self, ctx, *, vol: int):
        """Set the player volume."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        vol = max(min(vol, 1000), 0)
        controller.volume = vol

        await ctx.send(f'Setting the player volume to `{vol}`')
        await player.set_volume(vol)

    @commands.command(aliases=['np', 'current', 'nowplaying'], hidden=True)
    @commands.check(has_voted)
    async def now_playing(self, ctx):
        """Retrieve the currently playing song."""
        em = discord.Embed(color=self.bot.color)
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.current:
            return await ctx.send('I am not currently playing anything!')

        controller = self.get_controller(ctx)
        await controller.now_playing.delete()

        controller.now_playing = await ctx.send(f'Now playing: `{player.current}`')


    @commands.command(aliases=['q'], hidden=True)
    @commands.check(has_voted)
    async def queue(self, ctx):
        """Retrieve information on the next 5 songs from the queue."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if not player.current or not controller.queue._queue:
            return await ctx.send('There are no songs currently in the queue.', delete_after=20)

        upcoming = list(itertools.islice(controller.queue._queue, 0, 8))

        fmt = '\n'.join(f'**`{str(song.strack.name)}`*' for song in upcoming)
        count = 0
        line = ""
        for song in upcoming:
        	count += 1
        	line += f"{count}. {song.strack.name}\n"
        embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=line, color=self.bot.color)

        await ctx.send(embed=embed)

    @commands.command(aliases=['disconnect', 'dc'], hidden=True)
    @commands.check(has_voted)
    async def stop(self, ctx):
        """Stop and disconnect the player and controller."""
        player = self.bot.wavelink.get_player(ctx.guild.id)

        try:
            del self.controllers[ctx.guild.id]
        except KeyError:
            await player.disconnect()
            return await ctx.send('There was no controller to stop.')

        await self.bot.shards[ctx.guild.shard_id].ws.voice_state(str(ctx.guild.id), None)
        await ctx.send('Disconnected player and killed controller.', delete_after=20)

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def musicinfo(self, ctx):
        """Retrieve various Node/Server/Player information."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        node = player.node

        used = humanize.naturalsize(node.stats.memory_used)
        total = humanize.naturalsize(node.stats.memory_allocated)
        free = humanize.naturalsize(node.stats.memory_free)
        cpu = node.stats.cpu_cores

        fmt = f'**WaveLink:** `{wavelink.__version__}`\n\n' \
              f'Connected to `{len(self.bot.wavelink.nodes)}` nodes.\n' \
              f'Best available Node `{self.bot.wavelink.get_best_node().__repr__()}`\n' \
              f'`{len(self.bot.wavelink.players)}` players are distributed on nodes.\n' \
              f'`{node.stats.players}` players are distributed on server.\n' \
              f'`{node.stats.playing_players}` players are playing on server.\n\n' \
              f'Server Memory: `{used}/{total}` | `({free} free)`\n' \
              f'Server CPU: `{cpu}`\n\n' \
              f'Server Uptime: `{datetime.timedelta(milliseconds=node.stats.uptime)}`'
        await ctx.send(fmt)

   
    @skip.before_invoke
    @pause.before_invoke
    @resume.before_invoke
    async def checker(self, ctx):
    	player = self.bot.wavelink.get_player(ctx.guild.id)
       
    		
       
def setup(bot):
    bot.add_cog(Music(bot))
