from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
TG_TOKEN = '5277464061:AAGd9o-QlfQV0qQiF6reo5MjrdGkfUOlaOU'
bot = Bot(token=TG_TOKEN, parse_mode=types.ParseMode.HTML)
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())