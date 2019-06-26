import spotify
import asyncio
def setup(bot):
    @bot.event
    async def client_fix():
        if not bot.is_ready():
            return
        await bot.spclient.close()
        bot.spclient = None
        bot.spclient = spotify.Client('a3c571001085446eb8c28e7cf77a76cf', '58bcd0a71e354abe989a776ae0564fc0')
        await asyncio.sleep(1000)

    bot.loop.create_task(client_fix())
