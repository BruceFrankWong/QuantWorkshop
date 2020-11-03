# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List, Tuple, Union
from enum import Enum
import os
import csv
from datetime import date, timedelta


class ContractFre(Enum):
    CurrentMonth = 'CurrentMonth'   # 当月
    NextMonth = 'NextMonth'         # 下月
    QuarterMonth = 'QuarterMonth'   # 季月


def get_next_quarter_month(day: date, interval: int = 1) -> int:
    m: int = day.month
    return ((m-1)//3+1)//4


def czce_contract_series(cs: str) -> str:
    """
    郑州合约
    :param cs:
    :return:
    """
    return cs[1:]


def get_contract_of_current_month(day: date) -> str:
    """
    当前月份的合约。
    :param day:
    :return:
    """
    return day.strftime('%y%m')


def contract(day: date):
    pass


if __name__ == '__main__':
    futures_product_list = [
        'IF'
    ]
    futures_list = [
        {
            'IF':
                {
                    'exchange': 'CFFEX',
                    'symbol': 'IF',
                    'name': '沪深300股指期货',
                    'multiplier': 300,
                    'fluctuation': 0.2,
                }
        },
    ]
    d: date = date(2020, 11, 3)
    # contract(d)
    print(get_contract_of_current_month(d))
    print(get_contract_of_current_month(d, True))
