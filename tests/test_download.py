# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from datetime import date

from QuantWorkshop.types import QWPeriod,QWPeriodUnitType
from QuantWorkshop.download import download


# test
if __name__ == '__main__':
    p = QWPeriod(1, QWPeriodUnitType.Day)
    download('DCE.c2101', p, date(2020, 9, 30))

