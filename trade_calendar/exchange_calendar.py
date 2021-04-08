from data_api.tushare import api as tsapi
import datetime
import pandas as pd
from mydb import DBPool
today = datetime.datetime.now().date().strftime('%Y%M%d')


def get_calendar(exchange='SSE'):
    cal = tsapi.trade_cal(exchange=exchange, start_date='19900101', end_date=today)
    return cal


def get_hs_calendar():
    cal_sse = get_calendar('SSE')
    cal_szse = get_calendar('SZSE')
    return pd.concat([cal_sse, cal_szse])


def db_insert_trade_calendar(datas):
    sql = "INSERT INTO research.trade_calendar (exchange, cal_date, pretrade_date, is_open) " \
          "VALUES ( %s, STR_TO_DATE(%s, '%Y%m%d'), %s) ON DUPLICATE KEY UPDATE exchange=exchange;"
    try:
        conn = DBPool.get_connection()
        cur = conn.cursor()
        cur.executemany(sql, datas)
    except Exception:
        pass
    finally:
        conn.commit()
        cur.close()
        conn.close()


def db_insert_hs_calendar():
    cal = get_hs_calendar()
    datas = cal.values.tolist()
    datas = [(t[0], t[1], bool(t[2]))for t in datas]
    print('inserting trade_calendar to db')
    db_insert_trade_calendar(datas)
    print('insertion success')