import os
from loader import dp, bot
from aiogram import Bot, Dispatcher, types
from loader import dp, bot
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup


@dp.chat_join_request_handler()
async def checks(join_request: types.ChatJoinRequest):
    print(f'Принимаю реквест {join_request.from_user.first_name} в канале {join_request.chat.title}')
    await bot.approve_chat_join_request(chat_id=join_request.chat.id, user_id=join_request.from_user.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)