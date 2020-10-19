# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import pandas as pd

from QuantWorkshop.types import QWPeriod, QWPeriodUnitType
from QuantWorkshop.analysis.trend import zigzag, peak_valley_pivots
from QuantWorkshop.utility import load_data


if __name__ == '__main__':
    df: pd.DataFrame = load_data('SHFE.ag2012', QWPeriod(1, QWPeriodUnitType.Minute))
    zigzag(df)
    # peak_valley_pivots()
    # get_range('KQ.m@SHFE.ag', QWPeriod(1, QWPeriodUnitType.Day))
