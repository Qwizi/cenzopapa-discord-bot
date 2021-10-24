import os
#import httpx
from httpx import AsyncClient
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv
import ctypes
libgcc_s = ctypes.CDLL('libgcc_s.so.1')
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

@bot.event
async def on_ready():
    print("Online")
    print(await get_10_random_images())


@bot.command()
async def cenzo(ctx):
    image = await get_random_image()
    embed = send_embed_image(image.public_url)
    await ctx.send(embed=embed)


bot.run(TOKEN)
