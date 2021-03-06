import logging
import os
from check import job
from loader import dp, bot
import asyncio
import sqlite3
from config import db_path
from aiogram import Bot, Dispatcher, types
from loader import dp, bot
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
import re


class Enter_time(StatesGroup):
    enter_time = State()


@dp.chat_join_request_handler()
async def checks(join_request: types.ChatJoinRequest):
    db = sqlite3.connect(db_path)
    sql = db.cursor()
    action = sql.execute("SELECT action FROM behaviour").fetchone()[0]
    # print(times)
    if action == 'В реальном времени':
        print(f'Принимаю реквест {join_request.from_user.first_name} в канале {join_request.chat.title}')
        await bot.approve_chat_join_request(chat_id=join_request.chat.id, user_id=join_request.from_user.id)
    else:
        asyncio.create_task(job(chat_id=join_request.chat.id, user_id=join_request.from_user.id))

admin_id = [os.environ['id']]
ids = [int(i) for i in admin_id[0].split(", ")]

@dp.message_handler(commands='start')
async def start(message: types.Message):
    if message.from_user.id in ids:
        db = sqlite3.connect(db_path)
        sql = db.cursor()
        action = sql.execute("SELECT action FROM behaviour").fetchone()[0]
        time = sql.execute("SELECT time FROM behaviour").fetchone()[0]
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Изменить режим', callback_data='change'))
        await message.answer(text=f'''Приветствую🖐 \nРежим работы - {action} \nПринятие заявок через {time} минут''',
                             reply_markup=kb)


@dp.callback_query_handler(text='start')
async def start(call: types.CallbackQuery):
    if call.from_user.id in ids:
        db = sqlite3.connect(db_path)
        sql = db.cursor()
        action = sql.execute("SELECT action FROM behaviour").fetchone()[0]
        time = sql.execute("SELECT time FROM behaviour").fetchone()[0]
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Изменить режим', callback_data='change'))
        await bot.send_message(chat_id=call.from_user.id,
                               text=f'''Приветствую🖐 \nРежим работы - {action} \nПринятие заявок через {time} минут''',
                               reply_markup=kb)



@dp.callback_query_handler(text='change')
async def choose(call: types.CallbackQuery):
    if call.from_user.id in ids:
        kb = InlineKeyboardMarkup(row_width=1)
        bt1 = InlineKeyboardButton(text='В реальном времени', callback_data='realtime')
        bt2 = InlineKeyboardButton(text='Принятие заявок через время', callback_data='through')
        kb.add(bt1, bt2)
        await bot.send_message(chat_id=call.from_user.id, text='Выберите режим', reply_markup=kb)


@dp.callback_query_handler(text=['realtime', 'through'])
async def change(call: types.CallbackQuery):
    if call.from_user.id in ids:
        if call.data == 'realtime':
            db = sqlite3.connect(db_path)
            sql = db.cursor()
            sql.execute("UPDATE behaviour SET action = ?, time = ?", ('В реальном времени', 0))
            db.commit()
            kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='На главную', callback_data='start'))
            await bot.send_message(chat_id=call.from_user.id, text="Изменения приняты", reply_markup=kb)
    
        else:
            await bot.send_message(chat_id=call.from_user.id, text='Введите через сколько времени принимать заявки (мин)')
            await Enter_time.enter_time.set()


@dp.message_handler(state=Enter_time.enter_time)
async def enter_time(message: types.Message, state: FSMContext):
    if message.from_user.id in ids:
        await state.reset_state(with_data=False)
        time = message.text
        db = sqlite3.connect(db_path)
        sql = db.cursor()
        sql.execute("UPDATE behaviour SET action = ?, time = ?", ('Принятие через время', time))
        db.commit()
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='На главную', callback_data='start'))
        await message.answer("Изменения приняты", reply_markup=kb)
    






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
