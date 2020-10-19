# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from pathlib import Path
import json
import os
from datetime import date

import pandas as pd

from QuantWorkshop.config import CONFIGS
from QuantWorkshop.types import QWPeriod
from QuantWorkshop.download import download


# The path of the packages <QuantWorkshop>
packages_path: Path = Path(__file__).parent
packages_path_str: str = str(packages_path)


def load_json(json_file: Path) -> dict:
    with open(json_file, mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def save_json(data: dict, json_file: Path) -> None:
    with open(json_file, mode='w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_data(symbol: str, period: QWPeriod) -> pd.DataFrame:
    # 读取数据。
    csv_file: str = os.path.join(packages_path_str, CONFIGS['data_downloaded'], f'{symbol}_{period.to_english()}.csv')
    if not os.path.exists(csv_file):
        download(symbol, period, date(2016, 1, 1))
    return pd.read_csv(csv_file, index_col='datetime', parse_dates=True)
