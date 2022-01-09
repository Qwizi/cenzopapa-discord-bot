import asyncio
import disnake
import httpx
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()


from random import choice
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

            if hour == PAPA_HOUR and minutes == PAPA_MIN - 2:
                logger.info("Przygotowuje sie do 21:37")
                # Ustawiamy status na 21:37
                await bot.change_presence(activity=prepare_to_papa_hour)
                # Pobieramy 5 cenzo
                images = await get_random_images()
                # Czekamy na godzine papiezowa
                await asyncio.sleep(120)
                logger.info("Wysylam 5 losowych cenzo")
                #  Wysylamy 5 cenzo
                await send_random_images(images, bot.guilds)
                # Odczekujemy 2 minuty
                await asyncio.sleep(120)
                await bot.change_presence(activity=watching_kids)

            await asyncio.sleep(30)
    except (httpx.ConnectError, httpx.HTTPError):
        await asyncio.sleep(60)


@bot.slash_command(
    name="cenzo",
    description="Cenzo commands"
)
async def cenzo(ctx: disnake.ApplicationCommandInteraction):
    pass


@cenzo.sub_command(description="Send random cenzo")
async def random(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    try:
        logger.info("Pobieram loswe zdjecie")
        image = await get_random_image()
        logger.info(f"Pobralem losowe zdjecie {image.url}")
        if not image:
            raise httpx.HTTPError(message=API_ERROR)
        embed = await create_embed_image(image)
        logger.info(f"Wysyłam losowe zdjecie do {inter.author.name}")
        await inter.edit_original_message(embed=embed)
    except (httpx.ConnectError, httpx.HTTPError):
        await inter.edit_original_message(content=API_ERROR)


@cenzo.sub_command(description="Status")
async def status(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    status = [
        'Nie żyje',
        "Gryzie piach", 
        "Kopnął w kalendarz",
        "Dokonał żywota",
        "Przeniósł sie na tamten świat",
        "Zasnął na wieki",
        "Wyzionął ducha",
        "Przeniósł sie na łono Abrahama",
    ]
    if not inter.author.id == 418851232233553922:
        await inter.edit_original_message(content=choice(status))

@bot.event
async def on_ready():
    bot_guilds_len = len(bot.guilds)
    logger.info(f"Bot jest online")
    logger.info(f"Bot jest dodany na {bot_guilds_len} serwerach")
    await bot.change_presence(activity=watching_kids)


bot.loop.create_task(task_cenzo())
bot.run(TOKEN)
