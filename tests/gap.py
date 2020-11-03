# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List, Tuple, Union
from enum import Enum
import os
import csv
from datetime import date, timedelta


class Weekday(Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7


def futures() -> dict:
    """
    期货.
    """
    return {
        # 路径
        'IF': {
            'exchange': 'CFFEX',
            'name': '沪深300股指期货',
            'multiplier': 300,
            'fluctuation': 0.2,
            'last_trading_day_type': 'weekday',
            'last_trading_day_value': ['Friday', 3],
            'listed_contracts': [
                {
                    'period': 'month',
                    'postpone': 0,
                },
                {
                    'period': 'month',
                    'postpone': 1,
                },
                {
                    'period': 'quarter',
                    'postpone': 1,
                },
                {
                    'period': 'quarter',
                    'postpone': 2,
                },
            ],
            'listed_date': '2010-04-16',
            'first_listed_contracts': [
                '1005',
                '1006',
                '1009',
                '1012',
            ]
        },
    }


def get_weekday(year: int, month: int, weekday: int, n: int) -> date:
    """
    取得指定年月的第 n 个星期的日期。
    """
    weekday_of_first_day: int = date(year, month, 1).isoweekday()
    if weekday_of_first_day == weekday:
        return date(year, month, 1 + 7 * (n - 1))
    elif weekday_of_first_day > weekday:
        return date(year, month, weekday + 7 - weekday_of_first_day + 1 + 7 * (n - 1))
    else:
        return date(year, month, weekday - weekday_of_first_day + 1 + 7 * (n - 1))


class ContractFre(Enum):
    CurrentMonth = 'CurrentMonth'   # 当月
    NextMonth = 'NextMonth'         # 下月
    QuarterMonth = 'QuarterMonth'   # 季月


def get_next_quarter_month(day: date, interval: int = 1) -> int:
    m: int = day.month
    return ((m-1)//3+1)//4


def czce_contract_symbol(cs: str) -> str:
    """
    郑州合约
    :param cs:
    :return:
    """
    return cs[1:]


def get_contract_symbol(day: date) -> str:
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
    print(get_contract_symbol(d))
    year: int = 2020
    month: int = 11
    weekday: int = 5
    n: int = 3
    print(get_weekday(year, month, weekday, n), get_weekday(year, month, weekday, n).isoweekday())
    print(get_weekday(2020, 12, 5, 2), Weekday(get_weekday(2020, 11, 5, 2).isoweekday()))
