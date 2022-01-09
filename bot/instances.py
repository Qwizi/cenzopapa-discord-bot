import os
from disnake.activity import Game

import pytz
from cenzopapa import Cenzopapa
from disnake.ext import commands
from disnake import Activity, Game
from dotenv import load_dotenv
load_dotenv()
tz = pytz.timezone('Europe/Warsaw')

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')
LOCAL = os.getenv('LOCAL', 0)
PAPA_HOUR = os.getenv("PAPA_HOUR", 21)
PAPA_MIN = os.getenv("PAPA_MIN", 37)

API_ERROR = "Wystąpil problem z API"

api = Cenzopapa(API_URL)
bot = commands.Bot(command_prefix="??" if LOCAL == 1 else "?", test_guilds=[583717343255986178, 847524176054845440], sync_commands_debug=True)
watching_kids = Game(name='Dzieci')
prepare_to_papa_hour = Game(name='21:37')
die = Game(name='Nie zyje')
