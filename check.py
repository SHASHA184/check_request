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


async def job(chat_id, user_id):
    db = sqlite3.connect(db_path)
    sql = db.cursor()
    times = sql.execute("SELECT time FROM behaviour").fetchone()[0]
    await asyncio.sleep(times*60)
    await bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
    # tz = pytz.timezone('Europe/Kiev')
    # time_now = datetime.now(tz).strftime('%H:%M')
    # print(time_now)
    # id = sql.execute("SELECT id FROM requests WHERE action = ? AND time_check LIKE ?", (1, time_now)).fetchall()
    # for i in range(len(id)):
    #     sql.execute("UPDATE requests SET action = ? WHERE id = ? AND time_check LIKE ?", (0, id[i][0], time_now))
    #     channel_id = sql.execute("SELECT channel_id FROM requests WHERE id = ? AND time_check LIKE ?", (0, id[i][0], time_now)).fetchone()[0]
    #
    # db.commit()

# async def my_sleep_func():
#     await asyncio.sleep(random.randint(0, 5))
#
#
# async def display_date(num, loop):
#     end_time = loop.time() + 50.0
#     while True:
#         print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
#         if (loop.time() + 1.0) >= end_time:
#             break
#         await asyncio.sleep(60)
#
#

#


