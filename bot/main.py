import asyncio
from datetime import datetime

import httpx

from instances import bot, TOKEN, tz, API_ERROR
from utils import send_10_random_images, get_random_image, send_embed_image



@bot.command()
async def cenzo(ctx):
    try:
        image = await get_random_image()
        if not image:
            raise httpx.HTTPError(message=API_ERROR)
        embed = send_embed_image(image)
        await ctx.send(embed=embed)
    except (httpx.ConnectError, httpx.HTTPError):
        await ctx.send(API_ERROR)


async def task_cenzo():
    try:
        await bot.wait_until_ready()
        while not bot.is_closed():

            hour = int(datetime.now(tz).time().strftime("%H"))
            minutes = int(datetime.now(tz).time().strftime("%M"))
            print(f"{hour}:{minutes}")
            if hour == 21 and minutes == 37:
                await send_10_random_images(bot.guilds)

            await asyncio.sleep(60)
    except (httpx.ConnectError, httpx.HTTPError):
        await asyncio.sleep(60)


@bot.event
async def on_ready():
    bot_guilds_len = len(bot.guilds)
    print("Online")
    print(f"Bot jest dodany na {bot_guilds_len} serwerach")


bot.loop.create_task(task_cenzo())
bot.run(TOKEN)
