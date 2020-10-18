# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from QuantWorkshop.types import QWPeriod, QWPeriodUnitType
from QuantWorkshop.analysis.statistics import get_range


if __name__ == '__main__':
    get_range('KQ.m@SHFE.ag', QWPeriod(1, QWPeriodUnitType.Minute))
    # get_range('KQ.m@SHFE.ag', QWPeriod(1, QWPeriodUnitType.Day))
