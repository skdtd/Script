import sqlite3
import time

conn = sqlite3.connect("123.db")
cur = conn.cursor()
# cur.execute("""PRAGMA journal_mode=WAL""")
cur.execute("""CREATE TABLE IF NOT EXISTS [t_setting](
                    [key] TEXT PRIMARY KEY,
                    [value] TEXT)""")
conn.commit()

count = 0
while True:
    cur.execute("select * from t_setting")
    conn.commit()
    print(cur.fetchone())
