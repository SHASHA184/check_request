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
    try:
        user_channel_status = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        user_status = re.findall(r"\w*", str(user_channel_status))
        print(user_status[70], user_status[60])
        try:
            if user_status[70] != 'left':
                print('Уже подписан')
            # Условие для "подписанных"
            else:
                await bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
                # Условие для тех, кто не подписан
        except:
            if user_status[60] != 'left':
                print('Уже подписан')

                # Условие для "подписанных"
            else:
                await bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
                # Условие для тех, кто не подписан
    except NetworkError and TimeoutError:
        await asyncio.sleep(10)
        await bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)


