# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import pandas as pd

from QuantWorkshop.types import QWPeriod, QWPeriodUnitType
from QuantWorkshop.analysis.data import load_data
from QuantWorkshop.analysis.plot import plot
# from QuantWorkshop.plot import get_macd, get_kdj, plot


if __name__ == '__main__':
    df: pd.DataFrame = load_data('CZCE.PF105', QWPeriod(1, QWPeriodUnitType.Minute))
    df_cal: pd.DataFrame = pd.DataFrame.copy(df.loc['2020-10-23 21:00:00':'2020-10-23 22:59:00'])
    plot(df_cal)
    # print(df_cal)
