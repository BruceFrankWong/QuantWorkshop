# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from QuantWorkshop.types import QWPeriod, QWPeriodUnitType
from QuantWorkshop.analysis.trend import zigzag, peak_valley_pivots


if __name__ == '__main__':
    zigzag('SHFE.ag2012', QWPeriod(1, QWPeriodUnitType.Minute))
    peak_valley_pivots()
    # get_range('KQ.m@SHFE.ag', QWPeriod(1, QWPeriodUnitType.Day))
