import asyncio
import os
# import httpx
from datetime import datetime

from httpx import AsyncClient
from discord import Embed
from discord.ext import commands, tasks
from dotenv import load_dotenv
from schemas import Image

load_dotenv()

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')

bot = commands.Bot(command_prefix="?")


def send_embed_image(image_url) -> Embed:
    e = Embed(title="https://jebzpapy.tk")
    e.set_image(url=image_url)
    return e


async def get_random_image() -> Image or None:
    try:
        async with AsyncClient() as client:
            response = await client.get(f"{API_URL}/aimages/random/")
            if response.status_code == 200:
                data = response.json()
                print(data)
                if data and data['id'] and data['public_url']:
                    image = Image(id=data['id'], public_url=data['public_url'])
                    return image
            return None
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
    return next((x for x in guild.text_channels if x.position == 0), None)

@bot.event
async def on_ready():
    print("Online")
    for guild in bot.guilds:
        channel = await get_default_channel(guild)
        print(channel.id)

@bot.command()
async def cenzo(ctx):
    image = await get_random_image()
    embed = send_embed_image(image.public_url)
    await ctx.send(embed=embed)

async def send_random_10_images():
    await bot.wait_until_ready()
    while not bot.is_closed():

        hour = int(datetime.now().time().strftime("%H"))
        minutes = int(datetime.now().time().strftime("%M"))
        print(f"{hour}:{minutes}")
        if hour == 21 and minutes == 37:
            print('Rozpoczynamy godzine papierzowa')
            for guild in bot.guilds:
                default_channel = await get_default_channel(guild)
                channel = bot.get_channel(default_channel.id)
                random_images = await get_10_random_images()
                for image in random_images:
                    embed = send_embed_image(image.public_url)
                    await channel.send(embed=embed)

        await asyncio.sleep(60)

bot.loop.create_task(send_random_10_images())
bot.run(TOKEN)
