import asyncio
import httpx

from datetime import datetime
from instances import bot, TOKEN, tz, API_ERROR, PAPA_HOUR, PAPA_MIN, watching_kids, \
    prepare_to_papa_hour
from utils import send_random_images, get_random_image, create_embed_image, get_random_images, get_default_channel


async def task_cenzo():
    async def get_time():
        hour = int(datetime.now(tz).time().strftime("%H"))
        minutes = int(datetime.now(tz).time().strftime("%M"))
        return hour, minutes

    try:

        await bot.wait_until_ready()
        while not bot.is_closed():
            hour, minutes = await get_time()
            print(f"{hour}:{minutes}")

            if hour == PAPA_HOUR and minutes == PAPA_MIN - 2:
                print("Przygotowuje sie do 21:37")
                # Ustawiamy status na 21:37
                await bot.change_presence(activity=prepare_to_papa_hour)
                # Pobieramy 5 cenzo
                images = await get_random_images()
                # Czekamy na godzine papiezowa
                await asyncio.sleep(120)
                #  Wysylamy 5 cenzo
                await send_random_images(images, bot.guilds)
                # Odczekujemy 2 minuty
                await asyncio.sleep(120)
                await bot.change_presence(activity=watching_kids)
            await asyncio.sleep(30)
    except (httpx.ConnectError, httpx.HTTPError):

        await asyncio.sleep(60)

@bot.command()
async def cenzo(ctx):
    try:
        image = await get_random_image()
        if not image:
            raise httpx.HTTPError(message=API_ERROR)
        embed = await create_embed_image(image)
        await ctx.send(embed=embed)
    except (httpx.ConnectError, httpx.HTTPError):
        await ctx.send(API_ERROR)


@bot.command()
async def status(ctx):
    await ctx.send("Nie żyje")


@bot.event
async def on_ready():
    bot_guilds_len = len(bot.guilds)
    print("Online")
    print(f"Bot jest dodany na {bot_guilds_len} serwerach")
    await bot.change_presence(activity=watching_kids)
    print(await get_random_image())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    for x in message.mentions:
        if x == bot.user:
            await message.channel.send("A dostałes kiedyś z kremówki?")
    await bot.process_commands(message)

bot.loop.create_task(task_cenzo())
bot.run(TOKEN)
