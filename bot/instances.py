import os

import pytz
from cenzopapa import Cenzopapa
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
tz = pytz.timezone('Europe/Warsaw')

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')
API_ERROR = "Wystąpil problem z API"
api = Cenzopapa(API_URL)
bot = commands.Bot(command_prefix="?")
