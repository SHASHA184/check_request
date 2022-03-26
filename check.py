import asyncio
import sqlite3
from config import db_path
from loader import bot
from asyncio.exceptions import TimeoutError
from aiogram.utils.exceptions import NetworkError


async def job(chat_id, user_id):
    db = sqlite3.connect(db_path)
    sql = db.cursor()
    times = sql.execute("SELECT time FROM behaviour").fetchone()[0]
    await asyncio.sleep(times * 60)
    try:
        await bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
    except NetworkError and TimeoutError:
        await asyncio.sleep(10)
        await bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)


