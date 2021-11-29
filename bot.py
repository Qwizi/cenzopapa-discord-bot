import asyncio
import os
from datetime import datetime

import pytz

from cenzopapa import Cenzopapa
from cenzopapa.schemas import Image

from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

tz = pytz.timezone('Europe/Warsaw')

load_dotenv()

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')

bot = commands.Bot(command_prefix="?")

api = Cenzopapa(API_URL)


def send_embed_image(image_url) -> Embed:
    e = Embed(title="https://jebzpapy.netlify.com")
    e.set_image(url=image_url)
    return e


async def get_random_image() -> Image or None:
    try:
        image, _ = await api.image.random()
        print(image)
        return image
    except Exception as e:
        print(e)
        return None


async def get_10_random_images() -> list[Image] or []:
    images = []
    for i in range(10):
        image = await get_random_image()
        while image in images:
            image = await get_random_image()
        images.append(await get_random_image())
    return images


async def get_default_channel(guild):
    return next((x for x in guild.text_channels if x.position == 0 or x.position == 1), None)

async def send_10_random_images(guilds):
    print('Rozpoczynamy godzine papierzowa')
    for guild in guilds:
        default_channel = await get_default_channel(guild)
        channel = bot.get_channel(default_channel.id)
        random_images = await get_10_random_images()
        for image in random_images:
            embed = send_embed_image(image.public_url)
            await channel.send(embed=embed)

@bot.event
async def on_ready():
    print("Online")
    print(await get_random_image())
    for guild in bot.guilds:
        channel = await get_default_channel(guild)
        print(channel.id)


@bot.command()
async def cenzo(ctx):
    image = await get_random_image()
    embed = send_embed_image(image.url)
    await ctx.send(embed=embed)


async def send_random_10_images():
    await bot.wait_until_ready()
    while not bot.is_closed():

        hour = int(datetime.now(tz).time().strftime("%H"))
        minutes = int(datetime.now(tz).time().strftime("%M"))
        print(f"{hour}:{minutes}")
        if hour == 21 and minutes == 37:
            await send_10_random_images(bot.guilds)

        await asyncio.sleep(60)


bot.loop.create_task(send_random_10_images())
bot.run(TOKEN)
