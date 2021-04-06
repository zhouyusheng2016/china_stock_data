import pandas as pd


def data_frame_columns_col(df: pd.DataFrame):
    """
    将dataframe的col编排为insert时插入的目标列
    :param df:
    :return:
    """
    return '('+','.join(df.columns)+')'
