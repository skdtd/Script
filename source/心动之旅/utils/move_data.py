import sqlite3

conn = sqlite3.connect(r"C:\Users\34840\Desktop\live.db")
cursor = conn.cursor()
res = cursor.execute("select * from live").fetchall()
print(res[0])
res = [(x[2].replace("-", "/"), x[3], x[4]) for x in res]
print(len(res))
print(res)
conn = sqlite3.connect(r"C:\Users\34840\Desktop\宝藏猎人.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS [t_data](
                    [id] INTEGER PRIMARY KEY,
                    [date] TEXT NOT NULL,
                    [time_stamp] TEXT NOT NULL,
                    [res] TEXT NOT NULL)""")
conn.commit()
res = cursor.executemany("INSERT INTO t_data  (date, time_stamp, res) VALUES ((?),(?),(?))", res)
conn.commit()