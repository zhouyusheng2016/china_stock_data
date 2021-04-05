from data_api.tushare import api as tsapi
import pandas as pd


def get_stock_list():
    api_fields = ['ts_code', 'name', 'exchange', 'curr_type', 'market', 'list_status', 'list_date', 'delist_date', 'is_hs']
    db_fields = ['code', 'name',  'market', 'exchange', 'curr_type', 'list_status', 'list_date', 'delist_date', 'is_to_hk']
    mapping = {t[0]: t[1] for t in zip(api_fields, db_fields)}
    # 此处注意 list_status必须手动便利, 注意插入时需要选UPDATE
    l = tsapi.stock_basic(exchange='', list_status='L', fields=','.join(mapping.keys()))
    d = tsapi.stock_basic(exchange='', list_status='D', fields=','.join(mapping.keys()))
    p = tsapi.stock_basic(exchange='', list_status='P', fields=','.join(mapping.keys()))
    res = pd.concat([l, d, p])
    return res.rename(mapping, axis=1)