import httpx
from cenzopapa.schemas import Image
from discord import Embed

from instances import bot, api, API_ERROR


def send_embed_image(image: Image) -> Embed:
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
    try:
        for guild in guilds:
            default_channel = await get_default_channel(guild)
            channel = bot.get_channel(default_channel.id)
            random_images = await get_10_random_images()
            for image in random_images:
                embed = send_embed_image(image.url)
                await channel.send(embed=embed)
    except (httpx.ConnectError, httpx.HTTPError):
        for guild in guilds:
            default_channel = await get_default_channel(guild)
            channel = bot.get_channel(default_channel.id)
            await channel.send(API_ERROR)
