from data_api.tushare import api as tsapi
from mydb.pool import DBPool
import pandas as pd

api_fields = ['ts_code', 'name', 'exchange', 'curr_type', 'market', 'list_status', 'list_date', 'delist_date', 'is_hs']
db_fields = ['code', 'name', 'market', 'exchange', 'curr_type', 'list_status', 'list_date', 'delist_date', 'is_to_hk']


def get_stock_list():
    mapping = {t[0]: t[1] for t in zip(api_fields, db_fields)}
    # 此处注意 list_status必须手动便利, 注意插入时需要选UPDATE
    l = tsapi.stock_basic(exchange='', list_status='L', fields=','.join(mapping.keys()))
    d = tsapi.stock_basic(exchange='', list_status='D', fields=','.join(mapping.keys()))
    p = tsapi.stock_basic(exchange='', list_status='P', fields=','.join(mapping.keys()))
    res = pd.concat([l, d, p])
    return res.rename(mapping, axis=1)[db_fields]


def db_insert_stock_basic():
    fileds = ",".join(db_fields)

    stock_basic = get_stock_list()
    stock_basic = stock_basic.values.tolist()

    sql = "INSERT INTO research.stock_basic ("+fileds+") " \
          "VALUES (%s, %s, %s, %s, %s, %s, STR_TO_DATE(%s, '%Y%m%d'), STR_TO_DATE(%s, '%Y%m%d'), %s)"
    try:
        conn = DBPool.get_connection()
        cur = conn.cursor()
        cur.executemany(sql, stock_basic)
    except Exception as e:
        raise e
    finally:
        conn.commit()
        cur.close()
        conn.close()


if __name__ == '__main__':
    db_insert_stock_basic()