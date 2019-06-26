def setup(bot):
    @bot.event
    async def on_command(ctx):
        bot.stats["cmds_used"] += 1
        bot.stats[str(ctx.command)] += 1