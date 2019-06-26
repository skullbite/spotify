import discord
from copy import deepcopy
from utils.checks import is_owner
from discord.ext import commands
def setup(bot):
	@bot.command(hidden=True)
	@commands.check(is_owner)
	async def sudo(ctx, user: discord.User, *, command):
		"""Runs a command under someones name"""
		cmd = ctx.message
		cmd.author = user
		cmd.content = ctx.prefix + command
		
		await bot.process_commands(cmd)
