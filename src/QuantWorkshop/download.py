# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


"""
QuantWorkshop - download module.
"""


from typing import List
from contextlib import closing
# from logging import Logger

from datetime import date
import os.path

import pandas as pd
from tqsdk import TqApi, TqAuth
from tqsdk.tools import DataDownloader

from QuantWorkshop.config import CONFIGS
from QuantWorkshop.utility import packages_path_str
from QuantWorkshop.types import QWPeriod, QWPeriodUnitType


def download(symbol: str, period: QWPeriod, date_start: date, date_end: date = None):
    # download path
    download_path: str = os.path.join(packages_path_str, CONFIGS['data_downloaded'])
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    csv_file: str = os.path.join(download_path, f'{symbol}_{period.to_chinese()}.csv')

    # 天勤API
    tq_api: TqApi = TqApi(auth=TqAuth(CONFIGS['tq']['account'], CONFIGS['tq']['password']))

    task = DataDownloader(
        tq_api,
        symbol_list=symbol,
        dur_sec=period.to_second(),
        start_dt=date_start,
        end_dt=date_end if date_end else date.today(),
        csv_file_name=csv_file
    )

    # 下载。
    with closing(tq_api):
        while not task.is_finished():
            tq_api.wait_update()
            print(f'正在下载 [{symbol}] 的 {period.to_chinese()} 数据，已完成： {task.get_progress():,.3f}%。')

    # 处理 csv 文件的 column。
    column_list: List[str]
    df: pd.DataFrame = pd.read_csv(csv_file)
    if period.unit == QWPeriodUnitType.Tick:
        column_list = [
            'last_price', 'highest', 'lowest',
            'bid_price1', 'bid_volume1', 'ask_price1', 'ask_volume1',
            'volume', 'amount', 'open_interest'
        ]
    else:
        column_list = [
            'open', 'high', 'low', 'close', 'volume', 'open_oi', 'close_oi'
        ]
    for column in column_list:
        str_to_be_replaced = ''.join([symbol, '.', column])
        if str_to_be_replaced in df.columns:
            df.rename(columns={str_to_be_replaced: column}, inplace=True)
    df.to_csv(csv_file, index=False)


def download_from_list():
    pass


def download_from_csv():
    pass


def download_from_json():
    pass
