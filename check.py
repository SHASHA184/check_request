import asyncio
import os
import sqlite3
from datetime import datetime, timedelta

import aioschedule
import schedule
import time
from config import db_path
from loader import bot
import pytz


async def job():
    db = sqlite3.connect(db_path)
    sql = db.cursor()
    tz = pytz.timezone('Europe/Kiev')
    time_now = datetime.now(tz).strftime('%H:%M')
    print(time_now)
    id = sql.execute("SELECT id FROM requests WHERE action = ? AND time_check LIKE ?", (1, time_now)).fetchall()
    for i in range(len(id)):
        sql.execute("UPDATE requests SET action = ? WHERE id = ? AND time_check LIKE ?", (0, id[i][0], time_now))
        channel_id = sql.execute("SELECT channel_id FROM requests WHERE id = ? AND time_check LIKE ?", (0, id[i][0], time_now)).fetchone()[0]
        await bot.approve_chat_join_request(chat_id=channel_id, user_id=id[i][0])
    db.commit()


while True:
    asyncio.create_task(job())
    aioschedule.run_pending()
    asyncio.sleep(60)