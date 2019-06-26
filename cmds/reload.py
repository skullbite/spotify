from utils.checks import is_owner
from discord.ext import commands
import os
import discord
import traceback
import sys
def setup(bot):
    @bot.command(aliases=["re"], hidden=True)
    @commands.check(is_owner)
    async def reload(ctx, *, module):
        if module.lower() == "all":
            errors = []
            for x in os.listdir("cmds"):
                 if not x.endswith(".py"):
                     pass
                 else:
                     module = x[:-3]
                     try:
                         try:
                             bot.unload_extension(f"cmds.{module}")
                         except:
                             pass
                         bot.load_extension(f"cmds.{module}")
                     except Exception as e:
                         errors.append(f"{module}: `{e}`")
                     if errors != []:
                         extra = f":warning: **{len(errors)} Error(s) occured**:\n" + "\n".join(errors) 
                     else:
                         extra = ""
            events = len([x for x in os.listdir("cmds") if x.startswith('on_') or x.startswith('ev')])
            cmds = (len(os.listdir("cmds")) - events) - 1
            owo = discord.Embed(title=f"Reloading {cmds} Commands and {events} Events...", color=bot.color, description=extra)
            await ctx.send(embed=owo)
                         
        else:
            if "on_" in module or "ev_" in module:
                _type = "event"
            else:
                _type = "command"

            try:
                try:
                    bot.unload_extension(f"cmds.{module}")
                except:
                    pass
                bot.load_extension(f"cmds.{module}")
            except Exception as err:
                e = err
                _traceback = traceback.format_tb(e.__traceback__)
                _traceback = ''.join(_traceback)
                fullerror = ('```py\n{2}{0}: {3}\n```').format(type(e).__name__, ctx.message.content, _traceback, e)
                return await ctx.send(f"ERR: {fullerror}")

            await ctx.send(f"Reloaded {_type}: {module}")
