import sqlite3
from datetime import datetime, timedelta
import schedule
import time
from config import db_path


def job():
    print(0)
    db = sqlite3.connect(db_path)
    sql = db.cursor()
    time_now = datetime.now().strftime('%H:%M')
    id = sql.execute("SELECT id FROM requests WHERE action = ? AND time_check LIKE ?", (1, time_now)).fetchall()
    for i in range(len(id)):
        sql.execute("UPDATE requests SET action = ? WHERE id = ? AND time_check LIKE ?", (0, id[i][0], time_now))
    db.commit()


schedule.every(1).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)