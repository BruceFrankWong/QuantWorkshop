# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import os
from datetime import date

from QuantWorkshop.utility import packages_path_str
from QuantWorkshop.config import CONFIGS
from QuantWorkshop.types import QWPeriod, QWPeriodUnitType
from QuantWorkshop.download import download


def test_download():
    symbol: str = 'SHFE.ag2101'
    period: QWPeriod = QWPeriod(1, QWPeriodUnitType.Day)
    date_start: date = date(2020, 9, 30)
    csv_file: str = os.path.join(f'{packages_path_str}',
                                 CONFIGS['data_downloaded'],
                                 f'{symbol}_{period.to_english()}.csv'
                                 )
    if os.path.exists(csv_file):
        os.remove(csv_file)
    assert os.path.exists(csv_file) is False
    download(symbol=symbol, period=period, date_start=date_start)
    assert os.path.exists(csv_file) is True


if __name__ == '__main__':
    test_download()
