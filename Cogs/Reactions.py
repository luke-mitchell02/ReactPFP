import datetime
import math

import aiohttp
import requests
import io

from PIL import Image, ImageDraw

from discord.ext import commands, tasks

from Functions import SQL, Utilities


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #self.addPFP.start()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not self.bot.message:
            return

        if payload.member.bot:
            return

        if payload.message_id == self.bot.message.id:
            if not await SQL.select(f"SELECT User FROM Queue WHERE User = '{payload.member.id}'", one=True) and not await SQL.select(f"SELECT User FROM Reacted WHERE User = '{payload.member.id}'", one=True):
                if payload.member.avatar:
                    await SQL.execute(f"INSERT INTO Queue (User, Avatar, Timestamp) VALUES ('{payload.member.id}', '{payload.member.avatar.url}', '{datetime.datetime.utcnow()}')")

    @commands.command()
    async def sendHere(self, ctx):
        msg = await ctx.send(embed=Utilities.Embed("Blank"))

        await SQL.execute(f"UPDATE Other SET Channel = '{ctx.channel.id}', Message = '{msg.id}'")

    @commands.command()
    async def draw(self, ctx):
        await self.genImg()

    @tasks.loop(minutes=1)
    async def addPFP(self):
        await self.bot.wait_until_ready()
        await self.genImg()

    async def genImg(self):
        card = Image.open('Data/template.png')
        width, height = card.size
        draw = ImageDraw.Draw(card, "RGB")

        queue = await SQL.select("SELECT * FROM Queue", nested=True, dict=True)
        counter = await SQL.select("SELECT COUNT(*) FROM Reacted", one=True) or 0
        people = await SQL.select("SELECT People FROM Other", one=True)
        size = int(round(math.sqrt((width * height) / people), 2))

        img_per_row = round(width / size)
        max_rows = round(height / size)

        print(f"Width: {width}\nHeight: {height}\nPeople Wanted: {people}\nImage Size: {size}px²\nPer Row: {img_per_row}\nTotal Rows: {max_rows}\n")

        if queue:
            number_of_rows = math.floor(counter / img_per_row)
            number_on_row = counter - (number_of_rows * img_per_row)

            x = int(0 + (size * number_on_row))
            y = int(0 + (size * number_of_rows))

            for i in range(int(img_per_row * max_rows)):
                for row in queue:
                    url = row['Avatar']

                    if 'size' in url:
                        url = url.split('size=')[0] + "size=1024"

                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            resp = await response.read()

                            avatar = Image.open(io.BytesIO(resp)).resize((size, size))
                            rgb_avatar = avatar.convert("RGB")
                            card.paste(rgb_avatar, (x, y))
                            card.save(f'Data/test.png', quality=100)

                            counter += 1
                            x += size

                            if x == width:
                                y += size
                                x = 0


def setup(bot):
    bot.add_cog(Reactions(bot))
