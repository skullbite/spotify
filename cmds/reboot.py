from utils.checks import is_owner
from discord.ext import commands
import os
def setup(bot):
    @bot.command(aliases=["restart"], hidden=True)
    @commands.check(is_owner)
    async def reboot(ctx):
        """Restarts the process."""
        await ctx.send('Now restarting...')
        await bot.doge.send('*restart*')
        await bot.logout()