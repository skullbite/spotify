import discord
def setup(bot):
    @bot.event
    async def on_message(msg):
        if msg.content == bot.user.mention:
            await msg.channel.send("If you need something please use `sp!help`.")
        else:
            if not msg.author.bot:
                await bot.process_commands(msg)
