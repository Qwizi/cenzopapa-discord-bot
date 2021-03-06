import asyncio
from disnake.embeds import Embed
import httpx
from cenzopapa.schemas import Image
from instances import bot, api, API_ERROR, die


async def create_embed_image(image: Image) -> Embed:
    e = Embed(title=f"https://jebzpapy.netlify.com/cenzo/{image.id}")
    e.set_image(url=image.url)
    return e


async def get_random_image() -> Image or None:
    try:
        image, _ = await api.image.random()
        print(image)
        return image
    except Exception as e:
        print(e)
        return None


async def get_random_images(count=5) -> list[Image] or []:
    images = []
    for i in range(count):
        image = await get_random_image()
        while image in images:
            image = await get_random_image()
        images.append(image)
    return images


async def get_default_channel(guild):
    return next((x for x in guild.text_channels if x.permissions_for(guild.me).send_messages), None)


async def send_random_images(random_images, guilds):
    try:
        print(f"Pobralem {len(random_images)} cenzo")
        for guild in guilds:
            print(f"Zaczynam wysylac cenzo na serwerze {guild.name}")
            default_channel = await get_default_channel(guild)
            channel = bot.get_channel(default_channel.id)
            print(f"Domyslny kanal {channel.name}")
            for image in random_images:
                print(f"Wysłam zdjecie {image.url}")
                embed = await create_embed_image(image)
                await channel.send(embed=embed)
        await bot.change_presence(activity=die)
    except (httpx.ConnectError, httpx.HTTPError):
        for guild in guilds:
            default_channel = await get_default_channel(guild)
            channel = bot.get_channel(default_channel.id)
            await channel.send(API_ERROR)
        await asyncio.sleep(60)
