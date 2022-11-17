# coding: utf-8
import sqlite3
from unit.log import Log


class DB:
    COLORS = ["#000000", "#003300", "#006600", "#009900", "#00CC00", "#00FF00", "#330000", "#333300", "#336600",
              "#339900", "#33CC00", "#33FF00", "#660000", "#663300", "#666600", "#669900", "#66CC00", "#66FF00",
              "#990000", "#993300", "#996600", "#999900", "#99CC00", "#99FF00", "#CC0000", "#CC3300", "#CC6600",
              "#CC9900", "#CCCC00", "#CCFF00", "#FF0000", "#FF3300", "#FF6600", "#FF9900", "#FFCC00", "#FFFF00",
              "#000033", "#003333", "#006633", "#009933", "#00CC33", "#00FF33", "#330033", "#333333", "#336633",
              "#339933", "#33CC33", "#33FF33", "#660033", "#663333", "#666633", "#669933", "#66CC33", "#66FF33",
              "#990033", "#993333", "#996633", "#999933", "#99CC33", "#99FF33", "#CC0033", "#CC3333", "#CC6633",
              "#CC9933", "#CCCC33", "#CCFF33", "#FF0033", "#FF3333", "#FF6633", "#FF9933", "#FFCC33", "#FFFF33",
              "#000066", "#003366", "#006666", "#009966", "#00CC66", "#00FF66", "#330066", "#333366", "#336666",
              "#339966", "#33CC66", "#33FF66", "#660066", "#663366", "#666666", "#669966", "#66CC66", "#66FF66",
              "#990066", "#993366", "#996666", "#999966", "#99CC66", "#99FF66", "#CC0066", "#CC3366", "#CC6666",
              "#CC9966", "#CCCC66", "#CCFF66", "#FF0066", "#FF3366", "#FF6666", "#FF9966", "#FFCC66", "#FFFF66",
              "#000099", "#003399", "#006699", "#009999", "#00CC99", "#00FF99", "#330099", "#333399", "#336699",
              "#339999", "#33CC99", "#33FF99", "#660099", "#663399", "#666699", "#669999", "#66CC99", "#66FF99",
              "#990099", "#993399", "#996699", "#999999", "#99CC99", "#99FF99", "#CC0099", "#CC3399", "#CC6699",
              "#CC9999", "#CCCC99", "#CCFF99", "#FF0099", "#FF3399", "#FF6699", "#FF9999", "#FFCC99", "#FFFF99",
              "#0000CC", "#0033CC", "#0066CC", "#0099CC", "#00CCCC", "#00FFCC", "#3300CC", "#3333CC", "#3366CC",
              "#3399CC", "#33CCCC", "#33FFCC", "#6600CC", "#6633CC", "#6666CC", "#6699CC", "#66CCCC", "#66FFCC",
              "#9900CC", "#9933CC", "#9966CC", "#9999CC", "#99CCCC", "#99FFCC", "#CC00CC", "#CC33CC", "#CC66CC",
              "#CC99CC", "#CCCCCC", "#CCFFCC", "#FF00CC", "#FF33CC", "#FF66CC", "#FF99CC", "#FFCCCC", "#FFFFCC",
              "#0000FF", "#0033FF", "#0066FF", "#0099FF", "#00CCFF", "#00FFFF", "#3300FF", "#3333FF", "#3366FF",
              "#3399FF", "#33CCFF", "#33FFFF", "#6600FF", "#6633FF", "#6666FF", "#6699FF", "#66CCFF", "#66FFFF",
              "#9900FF", "#9933FF", "#9966FF", "#9999FF", "#99CCFF", "#99FFFF", "#CC00FF", "#CC33FF", "#CC66FF",
              "#CC99FF", "#CCCCFF", "#CCFFFF", "#FF00FF", "#FF33FF", "#FF66FF", "#FF99FF", "#FFCCFF", "#FFFFFF"]

    DATAS = ['大本营', '丛林', '沙漠', '峡谷', '海底', '孤岛', '沉船']
    # table
    DATA_TABLE = '''CREATE TABLE IF NOT EXISTS `live`( `id` INTEGER PRIMARY KEY, `room_num` VARCHAR(100) NOT NULL, `date` VARCHAR(100) NOT NULL, `time_stamp` VARCHAR(100) NOT NULL, `res` VARCHAR(100) NOT NULL, `url` VARCHAR(100) NOT NULL );'''
    COLORS_TABLE = '''CREATE TABLE IF NOT EXISTS `colors`( `color` VARCHAR(100) NOT NULL );'''
    MAP_TABLE = '''CREATE TABLE IF NOT EXISTS `map`( `res` VARCHAR(100) NOT NULL, `font` VARCHAR(100) NOT NULL, `bg` VARCHAR(100) NOT NULL );'''
    AD_TABLE = '''CREATE TABLE IF NOT EXISTS `ad`(`id` INTEGER PRIMARY KEY,`type` VARCHAR(10) NOT NULL, `enable` VARCHAR(10) NOT NULL, `content` VARCHAR(256) NOT NULL, `param` VARCHAR(256));'''
    # insert
    INSERT_DATA = '''INSERT INTO live ( `id`, `room_num`, `date`, `time_stamp`, `res`, `url` ) VALUES (NULL, ?, ?, ?, ?, ?);'''
    INSERT_COLOR = '''INSERT INTO colors ( `color` ) VALUES (?);'''
    INSERT_MAP = '''INSERT INTO map ( `res`, `font`, `bg` ) VALUES (?, "#000000", "#FFFFFF");'''
    INSERT_AD = '''insert into `ad` (`id`, `type`, `enable`, `content`, `param`) VALUES (NULL, ?, ?, ?, ?);'''
    # delete
    DELETE_AD = '''DELETE FROM `ad` WHERE `id` in (?)'''
    # update
    UPDATE_MAP = '''UPDATE map SET `font` = (?), `bg` = (?) WHERE `res` = (?)'''
    UPDATE_AD_DISABLE = '''UPDATE ad SET enable='0' WHERE "type"=(?) and enable='1';'''
    UPDATE_AD_ENABLE = '''UPDATE ad SET enable='1' WHERE "id"=(?)'''

    # select
    SELECT_AD = '''SELECT `id`, `type`, `enable`, `content`, `param` FROM `ad`;'''
    SELECT_ENABLE_AD = '''SELECT `id`, `type`, `enable`, `content`, `param` FROM `ad` where `enable` = '1';'''
    SELECT_DATA_BY_ID = '''SELECT * from live WHERE `id`=(?);'''
    SELECT_ALL_DATA = '''SELECT * from live;'''
    SELECT_BY_DATA = '''SELECT `live`.`id`, `map`.`font`, `map`.`bg`, `live`.`time_stamp`, `live`.`res` FROM `live` LEFT JOIN `map` ON `map`.`res` = `live`.`res` where `live`.`date` = (?) ORDER BY `live`.`id`;'''
    SELECT_DATA_LIST = '''select DISTINCT date from live;'''
    SELECT_ALL_COLOR = '''SELECT * from colors;'''
    SELECT_ALL_MAP = '''SELECT * from map;'''
    SELECT_MAP = '''select * from (SELECT `live`.`id`, `map`.`font`, `map`.`bg`, `live`.`time_stamp`, `live`.`res` FROM `live` LEFT JOIN `map` ON `map`.`res` = `live`.`res`ORDER BY `live`.`id` DESC LIMIT 120) t order by t.`id`;'''
    SELECT_DATA_COUNT = '''select `live`.`res`, count(`live`.`res`),`MAP`.`font`,`MAP`.`bg` from live LEFT JOIN `map` ON `MAP`.`res` = `live`.`res` where date in (?) group by `live`.`res`;'''

    def __init__(self, file_name):
        self.file_name = file_name
        self.cursor = None
        self.conn = None
        self.create_table(DB.DATA_TABLE)
        self.create_table(DB.COLORS_TABLE)
        self.create_table(DB.MAP_TABLE)
        self.create_table(DB.AD_TABLE)
        cs = [x[0] for x in self.select(self.SELECT_ALL_COLOR)]
        [self.COLORS.remove(x) for x in cs if x in self.COLORS]
        [self.insert(self.INSERT_COLOR, (x,)) for x in self.COLORS]
        res = self.select(DB.SELECT_ALL_MAP)
        if len(res) != 0:
            [DB.DATAS.remove(k) for k, _, _ in res if k in DB.DATAS]
        [self.insert(self.INSERT_MAP, (x,)) for x in DB.DATAS]

    def start(self):
        self.conn = sqlite3.connect(self.file_name)
        self.cursor = self.conn.cursor()

    def create_table(self, sql):
        try:
            self.start()
            self.cursor.execute(sql)
        except Exception as e:
            Log.warning('>> Create {}'.format(e))
        finally:
            self.close()

    def insert(self, sql, _data):
        try:
            self.start()
            self.cursor.execute(sql, _data)
            self.conn.commit()
            self.close()
            Log.info("插入SQL: {}, data: {}".format(sql, _data))
        except Exception as e:
            Log.warning('>> Insert {}'.format(e))

    def update(self, sql, _data):
        try:
            self.start()
            self.cursor.execute(sql, _data)
            self.conn.commit()
            self.close()
            Log.info("更新SQL: {}, data: {}".format(sql, _data))
        except Exception as e:
            Log.warning('>> Update Error: {}'.format(e))

    def select(self, sql, cond=None):
        self.start()
        if cond:
            self.cursor.execute(sql, cond)
        else:
            self.cursor.execute(sql)
        res = self.cursor.fetchall()
        self.close()
        Log.info("查询SQL: {}, condition: {}".format(sql, cond))
        return res

    def delete(self, sql, cond=None):
        self.start()
        if cond:
            self.cursor.execute(sql, cond)
        else:
            self.cursor.execute(sql)
        self.conn.commit()
        self.close()
        Log.info("删除SQL: {}, condition: {}".format(sql, cond))

    def close(self):
        self.cursor.close()
        self.conn.close()


class LiveEntry:
    def __init__(self, root_num, date, time_stamp, result, url):
        self.root_num = root_num
        self.date = date
        self.time_stamp = time_stamp
        self.result = result
        self.url = url

    def get_root_num(self):
        return self.root_num

    def get_date(self):
        return self.date

    def get_time_stamp(self):
        return self.time_stamp

    def get_result(self):
        return self.result

    def get_url(self):
        return self.url


class HuyaDao(DB):
    def __init__(self, file_name):
        DB.__init__(self, file_name=file_name)

    def insert_live(self, entry: LiveEntry):
        self.insert(DB.INSERT_DATA,
                    (entry.get_root_num(), entry.get_date(),
                     entry.get_time_stamp(), entry.get_result(), entry.get_url()))

    def select_date_count(self, _date):
        return self.select(DB.SELECT_DATA_COUNT, (_date,))

    def select_show_data(self):
        return self.select(DB.SELECT_MAP)

    def select_date(self):
        return self.select(DB.SELECT_DATA_LIST)

    def select_by_date(self, _date):
        return self.select(DB.SELECT_BY_DATA, (_date,))

    def select_all_map(self):
        return self.select(DB.SELECT_ALL_MAP)

    def insert_ad(self, _type, data, param):
        return self.insert(DB.INSERT_AD, (_type, '0', data, param,))

    def select_ad(self):
        return self.select(DB.SELECT_AD)

    def select_enable_ad(self):
        return self.select(DB.SELECT_ENABLE_AD)

    def deploy_ad(self, _type, _data):
        self.update(DB.UPDATE_AD_DISABLE, (_type,))
        return self.update(DB.UPDATE_AD_ENABLE, (_data,))

    def delete_ad(self, _data):
        return self.delete(DB.DELETE_AD, _data, )


if __name__ == "__main__":
    HuyaDao(r'C:\Users\Administrator\Desktop\Github\huya\live.db')
