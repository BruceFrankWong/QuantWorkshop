# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import os
from datetime import date

import pandas as pd

from QuantWorkshop.utility import packages_path_str
from QuantWorkshop.config import CONFIGS
from QuantWorkshop.types import QWPeriod
from QuantWorkshop.download import download


def load_data(symbol: str, period: QWPeriod) -> pd.DataFrame:
    # 读取数据。
    csv_file: str = os.path.join(packages_path_str, CONFIGS['data_downloaded'], f'{symbol}_{period.to_english()}.csv')
    if not os.path.exists(csv_file):
        download(symbol, period, date(2016, 1, 1))
    return pd.read_csv(csv_file, index_col='datetime', parse_dates=True)
