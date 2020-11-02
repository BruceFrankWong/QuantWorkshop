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
from QuantWorkshop.analysis.indicator import band_artifact


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


def do_backtest_band_artifact(symbol_list: List[str], period_list: List[QWPeriod]):
    for symbol in symbol_list:
        for period in period_list:
            # 加载数据
            df: pd.DataFrame = load_data(f'KQ.m@{symbol}', period)

            # 指标计算
            df['rsi_1'] = ta.RSI(df['close'], 6)
            df['rsi_2'] = ta.RSI(df['close'], 12)

            # WR 部分。
            df['wr'] = ta.WILLR(df['high'], df['low'], df['close'], 14)

            # 波段神器。
            df['ba'] = 100 + df['wr'] + df[['rsi_1', 'rsi_2']].max(axis=1)

            band_artifact(df)
            print(f'{symbol} on {period.to_english()}：')
            test_band_artifact_low(df)
            test_band_artifact_high(df)


if __name__ == '__main__':
    do_backtest_band_artifact(get_symbol_list(), get_period_list())
