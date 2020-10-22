# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import pandas as pd

from QuantWorkshop.types import QWPeriod, QWPeriodUnitType
from QuantWorkshop.analysis import load_data, zigzag, zigzag_hl
from QuantWorkshop.plot import plot


if __name__ == '__main__':
    df: pd.DataFrame = load_data('SHFE.ag2012', QWPeriod(1, QWPeriodUnitType.Minute))
    zigzag_hl(df.loc['2020-10-15 21:00:00':'2020-10-16 14:59:00'])
    # peak_valley_pivots()
    # get_range('KQ.m@SHFE.ag', QWPeriod(1, QWPeriodUnitType.Day))
    x: pd.DataFrame = pd.DataFrame.copy(df.loc['2020-10-15 21:00:00':'2020-10-16 14:59:00'])
    plot(x)
