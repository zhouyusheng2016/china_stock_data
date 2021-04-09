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


def get_one_stock_quote_between(code, start, end):
    """
    获取一个股票在start end之间的行情
    :param code:
    :param start:
    :param end:
    :return:
    """
    quotes = tsapi.daily(ts_code=code, start_date=start, end_date=end)
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


def db_insert_stock_quotes():
    pass


