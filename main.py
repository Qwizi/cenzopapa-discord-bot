import os
from dataclasses import dataclass

import httpx
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')

bot = commands.Bot(command_prefix="?")


@dataclass
class Image:
    id: int
    public_url: str


def send_embed_image(image_url) -> Embed:
    e = Embed(title="https://jebzpapy.tk")
    e.set_image(url=image_url)
    return e


async def get_random_image() -> Image:
    try:
        image = None
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/images/random/")
            if response.status_code == 200:
                data = response.json()
                print(data)
                if data and data['id'] and data['public_url']:
                    image = Image(id=data['id'], public_url=data['public_url'])
                    return image
    except Exception as e:
        print(e)


@bot.event
async def on_ready():
    print("jeszcze jak")


@bot.command()
async def cenzo(ctx):
    image = await get_random_image()
    embed = send_embed_image(image.public_url)
    await ctx.send(embed=embed)


bot.run(TOKEN)
