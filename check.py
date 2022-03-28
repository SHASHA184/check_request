import asyncio
import sqlite3
from config import db_path
from loader import bot
from asyncio.exceptions import TimeoutError
from aiogram.utils.exceptions import NetworkError
from loader import dp
import re


async def job(chat_id, user_id):
    db = sqlite3.connect(db_path)
    sql = db.cursor()
    times = sql.execute("SELECT time FROM behaviour").fetchone()[0]
    await asyncio.sleep(times * 60)
    async def accept():
        user_status = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        print(user_status["status"])
        if user_status["status"] != 'left':
            print('Уже подписан')
            # Условие для "подписанных"
        else:
            await bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
    try:
        await accept()
    except NetworkError and TimeoutError:
        await asyncio.sleep(10)
        await accept()


