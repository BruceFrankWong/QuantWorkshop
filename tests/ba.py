# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List, Tuple, Union
import os
import csv
from datetime import date, timedelta

import pandas as pd
import talib as ta
from openpyxl import Workbook

from QuantWorkshop.utility import packages_path_str
from QuantWorkshop.config import CONFIGS
from QuantWorkshop.download import download
from QuantWorkshop.types import QWPeriod, QWPeriodUnitType


def load_data(symbol: str, period: QWPeriod) -> pd.DataFrame:
    # 读取数据。
    csv_file: str = os.path.join(packages_path_str, CONFIGS['data_downloaded'], f'{symbol}_{period.to_english()}.csv')
    if not os.path.exists(csv_file):
        download(symbol, period, date(2016, 1, 1))
    return pd.read_csv(csv_file, parse_dates=True)


def get_symbol_list() -> List[str]:
    symbol_list = [
        'SHFE.au',
    ]
    return symbol_list


def get_period_list() -> List[QWPeriod]:
    period_list = [
        QWPeriod(1, QWPeriodUnitType.Day)
    ]
    return period_list


def group(data_list: List[int]) -> List[Tuple[int, int]]:
    result: List[Tuple[int, int]] = []
    first_consecutive: int = -1
    for idx in range(len(data_list) - 1):
        if data_list[idx] + 1 == data_list[idx+1]:
            if first_consecutive == -1:
                first_consecutive = data_list[idx]
        else:
            if first_consecutive == -1:
                result.append((data_list[idx], data_list[idx]))
            else:
                result.append((first_consecutive, data_list[idx]))
            first_consecutive = -1

    if first_consecutive != -1:
        result.append((data_list[-1], data_list[-1]))
    return result


def band_artifact_reverse_from_low(df: pd.DataFrame):
    # 源数据长度
    length: int = len(df)

    # 波段低点
    list_low_index: list = [x for x in df[df['ba'] <= 60].index]

    # 低点数量
    count_low_index: int = len(list_low_index)

    # 波段低点分组
    list_low_group: List[Tuple[int, int]] = group(list_low_index)
    dict_low: dict = {
        'begin': [x[0] for x in list_low_group],
        'end': [x[1] for x in list_low_group],
    }

    df_low: pd.DataFrame = pd.DataFrame(dict_low, dtype=int)
    df_low['length'] = df_low['end'] - df_low['begin'] + 1

    # 内存回收
    del list_low_index, list_low_group, dict_low

    # 其它column
    df_low['extreme_ba'] = 0  # 波段神器的极值
    df_low['extreme_high'] = 0  # 区间最高价的极值

    # df_low['open_delta_ba'] = 0  # 按照波段神器最低值买入，开仓偏移多少个周期。
    # df_low['close_delta_ba'] = 0  # 按照波段神器最低值买入，平仓偏移多少个周期。
    # df_low['price_open_ba'] = 0  # 按照波段神器最低值买入，开仓价理论值。
    # df_low['price_close_ba'] = 0  # 按照波段神器最低值买入，平仓价理论值。
    # df_low['open_type_ba'] = 0  # 按照波段神器最低值买入，开仓类型。1=反包，2=连续阳线。
    #
    # df_low['open_delta_high'] = 0  # 按照区间最高价的最低值买入，开仓偏移多少个周期。
    # df_low['close_delta_high'] = 0  # 按照区间最高价的最低值买入，平仓偏移多少个周期。
    # df_low['price_open_high'] = 0  # 按照区间最高价的最低值买入，开仓价理论值。
    # df_low['price_close_high'] = 0  # 按照区间最高价的最低值买入，平仓价理论值。
    # df_low['open_type_high'] = 0  # 按照区间最高价的最低值买入，开仓类型。1=反包，2=连续阳线。
    #
    # df_low['delta_ba_and_high'] = 0  # 区间最高价的最低值比波段神器极值点延后多少个周期。
    #
    # df_low['p&l_ba'] = 0  # 波段神器盈亏
    # df_low['p&l_high'] = 0  # 波段神器盈亏

    # 找出极值
    for idx in range(len(df_low)):
        if df_low.loc[idx, 'begin'] == df_low.loc[idx, 'end']:
            df_low.loc[idx, 'extreme_ba'] = df_low.loc[idx, 'begin']
            df_low.loc[idx, 'extreme_high'] = df_low.loc[idx, 'begin']
        else:
            extreme_ba = df.loc[df_low.loc[idx, 'begin']:df_low.loc[idx, 'end'], 'ba'].min()
            possible_index_list = df[df['ba'] == extreme_ba].index
            if len(possible_index_list) == 1:
                df_low.loc[idx, 'extreme_ba'] = possible_index_list[0]
                # print(df_low.loc[idx, 'extreme_ba'], type(possible_index_list))
            else:
                idx_begin = df.index[df_low.loc[idx, 'begin']]
                idx_end = df.index[df_low.loc[idx, 'end']]
                for idx_possible in possible_index_list:
                    if idx_begin <= idx_possible <= idx_end:
                        df_low.loc[idx, 'extreme_high'] = idx_possible
                        break
            df_low.loc[idx, 'extreme_ba'] = df[df['ba'] == extreme_ba].index
            print(df_low.loc[idx, 'extreme_ba'])

            extreme_high = df.iloc[df_low.iloc[idx]['begin']:df_low.iloc[idx]['end']]['high'].min()
            possible_index_list = df[df['high'] == extreme_high].index
            print(type(possible_index_list))
            if len(possible_index_list) == 1:
                df_low.loc[idx, 'extreme_high'] = df.index.get_loc(possible_index_list[0])
            else:
                idx_begin = df.index[df_low.loc[idx, 'begin']]
                idx_end = df.index[df_low.loc[idx, 'end']]
                for idx_possible in possible_index_list:
                    if idx_begin <= idx_possible <= idx_end:
                        df_low.loc[idx, 'extreme_high'] = idx_possible
                        break

    df_low['delta_ba_and_high'] = df_low['extreme_high'] - df_low['extreme_ba']

    print(df_low)


def band_artifact_reverse_from_high(df: pd.DataFrame):
    pass


def do_backtest_band_artifact(symbol_list: List[str], period_list: List[QWPeriod]):
    for symbol in symbol_list:
        for period in period_list:
            # 加载数据
            df: pd.DataFrame = load_data(f'KQ.m@{symbol}', period)

            # 指标计算
            # RSI
            df['rsi_1'] = ta.RSI(df['close'], 6)
            df['rsi_2'] = ta.RSI(df['close'], 12)
            # WR。
            df['wr'] = ta.WILLR(df['high'], df['low'], df['close'], 14)
            # 波段神器（BandArtifact）。
            df['ba'] = 100 + df['wr'] + df[['rsi_1', 'rsi_2']].max(axis=1)

            print(f'{symbol} on {period.to_english()}：')
            band_artifact_reverse_from_low(df)
            band_artifact_reverse_from_high(df)


if __name__ == '__main__':
    do_backtest_band_artifact(get_symbol_list(), get_period_list())
