import discord
from discord.ext import commands, tasks

from Functions import SQL


class Cache(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.createCache.start()

    def cog_unload(self):
        self.createCache.cancel()

    @tasks.loop(seconds=30)
    async def createCache(self):
        data = await SQL.select(f"SELECT * FROM React.Other", dict=True)

        if data['Channel']:
            channel = None
            try:
                channel = await self.bot.fetch_channel(int(data['Channel']))

                if channel:
                    self.bot.channel = channel
                else:
                    self.bot.channel = None

            except (discord.NotFound, discord.Forbidden):
                self.bot.channel = None
                await SQL.execute("UPDATE Other SET Channel = NULL")

            if channel and data['Message']:
                try:
                    message = await channel.fetch_message(int(data['Message']))

                    if message:
                        self.bot.message = message
                    else:
                        self.bot.message = None

                except (discord.NotFound, discord.Forbidden):
                    self.bot.message = None
                    await SQL.execute("UPDATE Other SET Message = NULL")


def setup(bot):
    bot.add_cog(Cache(bot))
