def setup(bot):
    @bot.event
    async def on_message_edit(before, after):
        if not after.author.bot:
            await bot.process_commands(after)