import traceback
import discord

from discord.ext import commands
from Functions import Utilities


class Errorhandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ignored = (commands.CommandNotFound, commands.NoPrivateMessage, commands.DisabledCommand, discord.NotFound, commands.BadArgument, discord.Forbidden, discord.HTTPException)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        attrerror = getattr(error, "original", error)

        if isinstance(attrerror, self.ignored):
            return

        elif isinstance(error, commands.MissingPermissions):
            try:
                return await ctx.send(embed=Utilities.Embed("Im not permitted to do that"))
            except discord.Forbidden:
                pass

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=Utilities.Embed(f"{ctx.author.mention}, you need to wait {Utilities.convertSeconds(error.retry_after)} before you can use this command again!"))

        # Unhandled

        await ctx.send(embed=Utilities.Embed(f"Something went wrong. Try again later"))
        channel = await self.bot.fetch_user(439327545557778433)

        result = "".join(traceback.format_exception(error, error, error.__traceback__))
        await channel.send(embed=Utilities.Embed(f"```py\n{result[:1800]}```\nCause:`{ctx.message.content}`\n[Jump]({ctx.message.jump_url})", colour=0xebc634, author=f"{ctx.author.name} ({ctx.author.id})", author_image=ctx.author.avatar.url))


def setup(bot):
    bot.add_cog(Errorhandler(bot))
