import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
TG_TOKEN = os.environ['Token']
bot = Bot(token=TG_TOKEN, parse_mode=types.ParseMode.HTML)
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())