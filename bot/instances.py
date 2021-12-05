import os
import discord
import pytz
from cenzopapa import Cenzopapa
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
tz = pytz.timezone('Europe/Warsaw')

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')
LOCAL = int(os.getenv('LOCAL'), 0)
PAPA_HOUR = int(os.getenv("PAPA_HOUR", 21))
PAPA_MIN = int(os.getenv("PAPA_MIN", 37))

API_ERROR = "Wystąpil problem z API"

api = Cenzopapa(API_URL)
bot = commands.Bot(command_prefix="??" if LOCAL else "?")
watching_kids = discord.Activity(name='Dzieci', type=discord.ActivityType.watching)
prepare_to_papa_hour = discord.Game(name='21:37')
die = discord.Game(name='Nie zyje')
