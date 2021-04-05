import sys
sys.path.append('/projects/china_stock_data')

import os
from config import CUR_PATH
from mydb.pool import DBPool


def create_stock_tables():
    """
    TODO: 目前不可用，因为mysql5.7.不可以给references权限

    :return:
    """
    fp = os.path.join(CUR_PATH, 'mydb/create_stock_tables.sql')
    with open(fp, 'r') as f:
        sqls = f.read()
    sql_sequence = sqls.split(';')
    # 建立数据库链接
    conn = DBPool.get_connection()
    cursor = conn.cursor()
    for sql in sql_sequence:
        cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    create_stock_tables()