from discord.ext.commands import errors
import discord
import traceback 
from utils import checks

async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
    else:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

    for page in _help:
        page = page.replace("```", "`")
        page = discord.Embed(title="Invalid argument.", description=page, color=0x1ed760)
        await ctx.send(embed=page)

def setup(bot):
    @bot.event
    async def on_command_error(ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            cmd = ctx.command
            help = " ".join([f"<{x}>" for x in cmd.clean_params])
            help = help
            desc = ('\n\n`' + cmd.help + '`' if cmd.help else '')
            helpem = discord.Embed(title="Invalid args.", description=f"`{ctx.prefix}{cmd} {help}`{desc}".replace(f"<@{bot.user.id}>", f"@{bot.user.name}").replace(f"<@!{bot.user.id}>", f"@{bot.user.name}"), color=bot.color)
            await ctx.send(embed=helpem)
        elif isinstance(err, discord.errors.Forbidden):
            pass
        elif isinstance(err, errors.CommandInvokeError):
            err = err.original
            if str(type(err).__name__) == "Forbidden" and "403" in str(err):
                return
            _traceback = traceback.format_tb(err.__traceback__)
            _traceback = ''.join(_traceback)
            fullerror = ('```py\n{2}{0}: {3}\n```').format(type(err).__name__, ctx.message.content, _traceback, err)
            shorterror = ('`{}` - `{}`').format(type(err).__name__, err)
            shorterrorem = discord.Embed(title=f"It appears an error has occured trying to run {ctx.command}.", color=bot.color)
            if not checks.is_owner(ctx):
               # shorterrorem.description = shorterror
                shorterrorem.set_footer(text="This error has been reported to my owner.")
                await bot.doge.send(embed=discord.Embed(description=f"Command: {ctx.command}\n{fullerror}", color=0x36393f).set_author(name="Command Error.", icon_url="https://cdn.discordapp.com/emojis/588404204369084456.png"))
            else:
                shorterrorem.description = fullerror

            await ctx.send(embed=shorterrorem)
        elif isinstance(err, errors.CheckFailure):
            em = discord.Embed(color=bot.color).set_author(name="Spotify", icon_url=bot.img)
            
            if ctx.command.checks[0].__qualname__ == "has_voted":
                em.description = f"To use this command you must [vote](https://discordbots.org/bot/{ctx.bot.user.id}/vote)."
            else:
                em.description = "You're not allowed to use this command."
            await ctx.send(embed=em)
        elif isinstance(err, errors.CommandNotFound):
            pass
        elif isinstance(err, errors.NoPrivateMessage):
            await ctx.send(embed=discord.Embed(color=bot.color, description="This command can't be used in dms.").set_author(name="Sorry :(", icon_url="https://cdn.discordapp.com/emojis/585861960613101573.gif?v=1"))
