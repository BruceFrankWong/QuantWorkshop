# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import os
from datetime import date

import pandas as pd
import numpy as np
import scipy.stats as st
from matplotlib import pyplot as plt

from QuantWorkshop.types import QWPeriod, QWPeriodUnitType
from QuantWorkshop.utility import packages_path_str
from QuantWorkshop.config import CONFIGS
from QuantWorkshop.download import download


def statistics_by_month(symbol: str):
    """
    在主力连续的日线上，统计各月涨跌情况。
    """
    pass


def get_range(symbol: str, period: QWPeriod):
    """
    统计涨跌幅。
    """
    csv_file: str = os.path.join(packages_path_str, CONFIGS['data_downloaded'], f'{symbol}_{period.to_english()}.csv')
    if not os.path.exists(csv_file):
        download(symbol, period, date(2016, 1, 1))
    df = pd.read_csv(csv_file)
    df['range_max'] = df['high'] - df['low']        # 最高价和最低价之间的波动
    df['range_oc'] = df['close'] - df['open']       # 收盘价和开盘价之间的波动
    print(f"最大值:\t{df['range_max'].max()}")
    print(f"方差:\t{df['range_max'].var()}")
    print(f"标准差:\t{df['range_max'].std()}")
    mean, std = df['range_max'].mean(), df['range_max'].std(ddof=1)
    conf_interval = st.norm.interval(0.9, loc=mean, scale=std)
    print(conf_interval)

    x = np.arange(-5, 5, 0.001)
    # PDF是概率密度函数
    y = st.norm.pdf(x, loc=mean, scale=std)
    plt.plot(x, y)
    plt.show()
