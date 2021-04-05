from data_api.tushare import api as tsapi
import datetime
import pandas as pd

today = datetime.datetime.now().date().strftime('%Y%M%d')


def get_calendar(exchange='SSE'):
    cal = tsapi.trade_cal(exchange=exchange, start_date='19900101', end_date=today)
    return cal


def get_hs_calendar():
    cal_sse = get_calendar('SSE')
    cal_szse = get_calendar('SZSE')
    return pd.concat([cal_sse, cal_szse])
