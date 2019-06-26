import ast
import discord

from discord.ext import commands
from utils.checks import is_owner


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

def setup(bot):
    @bot.command(name="eval", hidden=True, aliases=["ev"])
    @commands.check(is_owner)
    async def eval_fn(ctx, *, cmd):
        """uwu
    """
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        try:
            result = (await eval(f"{fn_name}()", env))
        except Exception as e:
        	return await ctx.send(f"ERR: `{e}`")
        try:
            await ctx.send(result)
        except Exception as e:
            if result == None:
                await ctx.send(f"`{e}`")
            elif not result:
                await ctx.send("`No Return.`")
            