import discord

from discord.ext import commands

from Functions import Utilities


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_message(message):
    if not message.guild:
        return

    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}\n{len(bot.extensions)} Modules Loaded')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Reactions roll in"))


Utilities.run(bot)
