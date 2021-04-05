from data_api.tushare import api as tsapi
import pandas as pd


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
