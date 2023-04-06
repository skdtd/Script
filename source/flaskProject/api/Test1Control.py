import sqlite3

conn = sqlite3.connect("123.db")
cur = conn.cursor()
# cur.execute("""PRAGMA journal_mode=WAL""")
cur.execute("""CREATE TABLE IF NOT EXISTS [t_setting](
                    [key] TEXT PRIMARY KEY,
                    [value] TEXT)""")
conn.commit()

count = 0
while True:
    cur.execute("insert into t_setting values ((?),(?))", (count, "1" * 1024))
    count = count + 1
    print(count)
    conn.commit()
