import datetime
import json
import os

from collections import namedtuple

import discord

from Functions import SQL


def configObjectify(config):
    with open(config, encoding="utf8") as data:
        return json.load(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values()))


def getConfig():
    return configObjectify('Data/cfg.json')


config = getConfig()
colour = 0xe4ebe8


def run(bot):
    bot.remove_command('help')
    bot.colour = colour
    bot.development = config.development
    bot.developer = config.developer

    bot.cache, bot.temp = {}, {}

    if not bot.development:
        bot.load_extension("Functions.Errors")

    for file in os.listdir(f"Cogs"):
        if file.endswith(".py"):
            bot.load_extension(f"Cogs.{file[:-3]}")

    try:
        bot.run(config.token, reconnect=True)
    except KeyboardInterrupt:
        return


async def Log(userid, log):
    await SQL.execute(f"INSERT INTO Logs (User, Log, Timestamp) VALUES ('{userid}', '{log}', '{datetime.datetime.utcnow()}')")


def Embed(description='', title='', footer='', development=False, thumbnail=None, image=None, colour=colour, author=None, author_image=None, timestamp=False, footer_icon=None, url=""):
    embed = discord.Embed(title=title, description=description, colour=colour, url=url)

    if image:
        embed.set_image(url=image)

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    if footer:
        if footer_icon:
            embed.set_footer(text=footer, icon_url=footer_icon)
        else:
            embed.set_footer(text=footer)

    if author:
        if author_image:
            embed.set_author(name=author, icon_url=author_image)
        else:
            embed.set_author(name=author)

    if timestamp:
        embed.timestamp = datetime.datetime.utcnow()

    return embed


def convertSeconds(seconds, range=7, short=False):
    seconds = int(seconds)

    intervals = (
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1),
    )

    if seconds < 1:
        return '0 seconds'

    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')

            result.append("{} {}".format(value, name))

    return ', '.join(result[:range])
