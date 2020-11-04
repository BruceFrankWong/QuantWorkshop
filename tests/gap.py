# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List, Tuple, Union
from enum import Enum
import os
import csv
from datetime import date, timedelta

from openpyxl import Workbook

from QuantWorkshop.utility import packages_path_str


def get_holiday_list() -> Tuple[List[Tuple[date, date, str]], List[date]]:
    result_range: List[Tuple[date, date, str]] = []
    result_expand: List[date] = []
    csv_path: str = os.path.join(packages_path_str, 'initial_data', 'holiday.csv')
    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            holiday_begin = date.fromisoformat(row['begin'])
            holiday_end = date.fromisoformat(row['end'])
            holiday_reason = row['reason']
            result_range.append((holiday_begin, holiday_end, holiday_reason))
            if holiday_begin == holiday_end:
                result_expand.append(holiday_begin)
            else:
                day = holiday_begin
                while day <= holiday_end:
                    result_expand.append(day)
                    day = day + timedelta(days=1)
    return result_range, result_expand


HOLIDAY_RANGE_LIST, HOLIDAY_EXPAND_LIST = get_holiday_list()

print(HOLIDAY_RANGE_LIST)
print(HOLIDAY_EXPAND_LIST)


def is_trading_day(day: date) -> bool:
    if day.isoweekday() == 6 or day.isoweekday() == 7:
        return False
    if day in HOLIDAY_EXPAND_LIST:
        return False
    else:
        return True


def is_holiday(day: date) -> bool:
    if day.isoweekday() == 6 or day.isoweekday() == 7:
        return True
    if day in HOLIDAY_EXPAND_LIST:
        return True
    else:
        return False


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
            'last_trading_day_value': [5, 3],
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
            'first_listed_date': '2010-04-16',
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


def is_contract_expired(product: str, contract: str) -> bool:
    pass


def get_if_contracts():
    product = futures()['IF']
    day: date = date.fromisoformat(product['first_listed_date'])

    contract_list = [{'symbol': f'IF{x}', 'listed_date': day} for x in product['first_listed_contracts']]
    for contract in contract_list:
        contract['expiration_date'] = get_weekday(int(f"20{contract['symbol'][2:4]}"),
                                                  int(contract['symbol'][4:]),
                                                  product['last_trading_day_value'][0],
                                                  product['last_trading_day_value'][1]
                                                  )
    for contract in contract_list:
        print(contract)

    while day <= date.today():
        if is_trading_day(day):
            pass
        day = day + timedelta(days=1)


if __name__ == '__main__':
    futures_product_list = [
        # 中金所
        'IF',
        'IH',
        'IC',
        'TF',
        'T',
        'TS',
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
    get_if_contracts()
