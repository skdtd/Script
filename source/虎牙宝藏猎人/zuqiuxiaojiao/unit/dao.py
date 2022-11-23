# coding: utf-8
import sqlite3

class DB:
    '''
    CREATE TABLE IF NOT EXISTS `t_zuqiu`(
`id` INTEGER PRIMARY KEY,
`date` TEXT NOT NULL,
`time_stamp` TEXT NOT NULL,
`res` TEXT NOT NULL)

CREATE TABLE IF NOT EXISTS `t_color`(
`res` TEXT NOT NULL,
`alias` TEXT NOT NULL,
`font` TEXT NOT NULL,
`bg` TEXT NOT NULL
)

select id, res, alias, font ,bg , date ,time_stamp from (select tz.id, tc.res, tc.alias, tc.font ,tc.bg , tz.date ,tz.time_stamp  FROM t_color tc left join t_zuqiu tz on tc.res = tz.res ORDER BY tz.id  DESC LIMIT 3 ) ORDER BY id

    '''

    # table
    DATA_TABLE = '''CREATE TABLE IF NOT EXISTS `live`( `id` INTEGER PRIMARY KEY, `room_num` VARCHAR(100) NOT NULL, `date` VARCHAR(100) NOT NULL, `time_stamp` VARCHAR(100) NOT NULL, `res` VARCHAR(100) NOT NULL, `url` VARCHAR(100) NOT NULL )'''
    COLORS_TABLE = '''CREATE TABLE IF NOT EXISTS `colors`( `color` VARCHAR(100) NOT NULL );'''
    # insert
    INSERT_DATA = '''INSERT INTO live ( `id`, `room_num`, `date`, `time_stamp`, `res`, `url` ) VALUES (NULL, ?, ?, ?, ?, ?);'''
    INSERT_COLOR = '''INSERT INTO colors ( `color` ) VALUES (?);'''
    INSERT_MAP = '''INSERT INTO map ( `res`, `font`, `bg` ) VALUES (?, "#000000", "#FFFFFF");'''
    INSERT_AD = '''insert into `ad` (`id`, `type`, `enable`, `content`, `param`) VALUES (NULL, ?, ?, ?, ?);'''
    # select
    SELECT_DATA = '''select id, res, alias, font ,bg , date ,time_stamp from (select tz.id, tc.res, tc.alias, tc.font ,tc.bg , tz.date ,tz.time_stamp  FROM t_color tc left join t_zuqiu tz on tc.res = tz.res ORDER BY tz.id  DESC LIMIT 3 ) ORDER BY id'''
    def __init__(self, file_name):
        self.file_name = file_name
        self.cursor = None
        self.conn = None
        self.create_table(DB.DATA_TABLE)
        self.create_table(DB.COLORS_TABLE)

    def start(self):
        self.conn = sqlite3.connect(self.file_name)
        self.cursor = self.conn.cursor()

    def create_table(self, sql):
        try:
            self.start()
            self.cursor.execute(sql)
        except Exception:
            pass
        finally:
            self.close()

    def insert(self, sql, _data):
        try:
            self.start()
            self.cursor.execute(sql, _data)
            self.conn.commit()
            self.close()
        except Exception:
            pass

    def update(self, sql, _data):
        try:
            self.start()
            self.cursor.execute(sql, _data)
            self.conn.commit()
            self.close()
        except Exception:
            pass

    def select(self, sql, cond=None):
        self.start()
        if cond:
            self.cursor.execute(sql, cond)
        else:
            self.cursor.execute(sql)
        res = self.cursor.fetchall()
        self.close()
        return res

    def delete(self, sql, cond=None):
        self.start()
        if cond:
            self.cursor.execute(sql, cond)
        else:
            self.cursor.execute(sql)
        self.conn.commit()
        self.close()

    def close(self):
        self.cursor.close()
        self.conn.close()


class ZuqiuDao(DB):
    def __init__(self, file_name):
        DB.__init__(self, file_name=file_name)



if __name__ == "__main__":
    ZuqiuDao(r"C:\Users\34840\Desktop\zuqiu.db")
