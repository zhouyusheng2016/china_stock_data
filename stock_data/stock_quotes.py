from data_api.tushare import api as tsapi
import pandas as pd
from mydb.pool import DBPool


def get_one_stock_quote_all(code):
    """
    获取一个股票的所有历史
    :param code:
    :return:
    """
    quotes = tsapi.daily(ts_code=code)
    return quotes.rename({'ts_code': 'code'}, axis=1)


def get_one_stock_quote_from(code, start):
    """
    获取一个股票在start end之间的行情
    :param code:
    :param start:
    :param end:
    :return:
    """
    quotes = tsapi.daily(ts_code=code, start_date=start)
    return quotes.rename({'ts_code': 'code'}, axis=1)


def get_one_day_quotes(td):
    """
    获取某个交易日的所有股票行情
    :param td:
    :return:
    """
    quotes = tsapi.daily(trade_date=td)
    return quotes.rename({'ts_code': 'code'}, axis=1)


def get_db_table_col():
    """
    获取股票数据表col
    :return:
    """
    sql = "SHOW COLUMNS FROM research.stock_daily_quotes; "
    try:
        conn = DBPool.get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        cb = cur.fetchall()
    except Exception as e:
        raise e
    finally:
        cur.close()
        conn.close()
    return [t[0] for t in cb]


def get_need_update_info():
    """
    获取数据库中需要更新的股票行情
    :return:
    """
    sql = "SELECT t1.code, t2.max_td, list_date, delist_date, list_status " \
          "FROM " \
          "(SELECT code, list_date, delist_date, list_status FROM research.stock_basic) as t1 " \
          "LEFT JOIN " \
          "(SELECT code, max(trade_date) as max_td FROM research.stock_daily_quotes GROUP BY code) as t2 " \
          "ON t1.code = t2.code " \
          "WHERE " \
          "(" \
              "t2.max_td < SUBDATE(CURDATE(), 1) " \
              "AND SUBDATE(CURDATE(), 1) IN (SELECT cal_date FROM research.trade_calendar WHERE is_open = 1 AND cal_date >= list_date )" \
              "AND IF(t1.list_status = 'D' and t2.max_td < t1.delist_date, TRUE,  FALSE)" \
          ") OR t2.max_td is NULL; "
    try:
        conn = DBPool.get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        cb = cur.fetchall()
    except Exception as e:
        raise e
    finally:
        cur.close()
        conn.close()
    return cb


def db_insert_datas(datas):
    """
    db插入stok quotes
    :param datas:
    :return:
    """
    db_col = ','.join(get_db_table_col())
    sql = "INSERT INTO research.stock_daily_quotes (" + db_col +") " \
          "VALUES(%s, STR_TO_DATE(%s, '%Y%m%d'), %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
          "ON DUPLICATE KEY UPDATE code = code; "

    try:
        print('insert in to stock_quotes')
        conn = DBPool.get_connection()
        cur = conn.cursor()
        cur.executemany(sql, datas)
        conn.commit()
        print('insertion done')
    except Exception as e:
        raise e
    finally:
        cur.close()
        conn.close()


def service_insert_stock_quotes():

    need_update = get_need_update_info()

    # 获取行情
    for info in need_update:
        code = info[0]
        db_td = info[1]
        list_dt = info[2]
        delist_dt = info[3]
        list_status = info[4]

        start_dt = db_td
        if db_td is None:
            start_dt = list_dt

        quotes = get_one_stock_quote_from(code, start_dt.strftime(start_dt, '%Y%m%d'))


