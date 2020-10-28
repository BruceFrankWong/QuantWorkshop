# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List, Tuple, Union
import os
import csv
from datetime import date, timedelta

import pandas as pd

from QuantWorkshop.utility import packages_path_str
from QuantWorkshop.types import QWPeriod, QWPeriodUnitType
from QuantWorkshop.analysis import load_data
from QuantWorkshop.analysis.indicator import wave


def get_holiday_list() -> List[Tuple[date, date, str]]:
    result: List[Tuple[date, date, str]] = []
    csv_path: str = os.path.join(packages_path_str, 'initial_data', 'holiday.csv')
    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            holiday_begin = date.fromisoformat(row['begin'])
            holiday_end = date.fromisoformat(row['end'])
            holiday_reason = row['reason']
            result.append((holiday_begin, holiday_end, holiday_reason))
    return result


def expand_day_range(day_range: Union[Tuple[date, date], Tuple[date, date, str]]) -> List[date]:
    if day_range[1] == day_range[0]:
        return [day_range[0]]
    else:
        result: List[date] = []
        day = day_range[0]
        while day <= day_range[1]:
            result.append(day)
            day = day + timedelta(days=1)
        return result


def shrink_day_range(day_range: List[date]) -> List[Tuple[date, date]]:
    result: List[Tuple[date, date]] = []
    begin: int = 0
    length: int = 0
    flag: bool = False

    for idx in range(len(day_range) - 1):
        if is_consecutive(day_range[idx], day_range[idx + 1]):
            if flag:
                length += 1
            else:
                begin = idx
                flag = True
        else:
            if flag:
                length += 1
            result.append((day_range[begin], day_range[begin+length]))
            flag = False
            length = 0
            begin = idx + 1

    if flag:
        length += 1
    result.append((day_range[begin], day_range[begin+length]))

    return result


def is_trading_day(day: date) -> bool:
    if day.isoweekday() == 6 or day.isoweekday() == 7:
        return False
    holiday_list: list = []
    for item in get_holiday_list():
        holiday_list.extend(expand_day_range(item))
    if day in holiday_list:
        return False
    else:
        return True


def is_holiday(day: date) -> bool:
    return not is_trading_day(day)


def next_trading_day(day: date) -> date:
    i: int = 1
    next_day: date = day + timedelta(days=i)
    while not is_trading_day(next_day):
        i += 1
        next_day: date = day + timedelta(days=i)
    return next_day


def is_consecutive(day_1: date, day_2: date) -> bool:
    if day_1 > day_2:
        day_1, day_2 = day_2, day_1

    if next_trading_day(day_1) == day_2:
        return True
    else:
        return False


def test_wave_trend(symbol: str, period: QWPeriod):
    wave_low_index: list = []
    wave_low_date: list = []
    wave_high_index: list = []
    wave_high_date: list = []
    result_low: list = []

    df: pd.DataFrame = load_data(f'KQ.m@{symbol}', period)
    wave(df)
    length: int = len(df)
    for idx in range(length):
        if df.iloc[idx]['wave'] < 60:
            wave_low_index.append(idx)
            wave_low_date.append(df.index[idx].date())
            # print(f'{df.index[idx].date()}, 低于 60。')
        if df.iloc[idx]['wave'] > 170:
            wave_high_index.append(idx)
            wave_high_date.append(df.index[idx].date())
            # print(f'{df.index[idx].date()}, 高于 170。')

    # 消除连续
    wave_low_filtered: List[Tuple[date, date]] = shrink_day_range(wave_low_date)
    wave_high_filtered: List[Tuple[date, date]] = shrink_day_range(wave_high_date)
    # for item in wave_low_filtered:
    #     print(item)

    print(f'{symbol}：')
    print(f'自 {df.index[0].date()} 至 {df.index[-1].date()}，共 {len(df)} 个交易日。')
    print(f'低于 60 的日期共有 {len(wave_low_index)}/{len(wave_low_date)} 个，占比{len(wave_low_index) / len(df) * 100:.3f}%；')
    print(f'高于 170 的日期共有 {len(wave_high_index)} 个，占比{len(wave_high_index) / len(df) * 100:.3f}%。')
    print(f'低于 60 的日期共有 {len(wave_low_filtered)} 段；')
    print(f'高于 170 的日期共有 {len(wave_high_filtered)} 段。')

    # print(df.loc['2020-10-09'])
    print('=' * 20)

    # for x in wave_low_date:
    #     print(x.isoformat())
    # for x in wave_low_filtered:
    #     print(x)

    # 找出极值
    for item in wave_low_filtered:
        print(f'{item}, 在日期 {item[0]} 至 {item[1]} 的区间中：')
        day_list = expand_day_range(item)
        wave_min = df.loc[item[0].isoformat():item[1].isoformat(), 'wave'].min()
        print(df[df['wave'] == wave_min])

    # for idx in wave_low_index:
    #     close = df.iloc[idx]['close']
    #     i: int = 0
    #     if df.iloc[idx+i-1]['close'] > df.iloc[idx+i]['close']:
    #         while df.iloc[idx+i-1]['high'] < df.iloc[idx+i]['high'] < df.iloc[idx+i+1]['high']:
    #             i += 1
    #         result_low.append((df.index[idx], i))
    #     else:
    #         result_low.append((df.index[idx], -1))
    # for item in result_low:
    #     print(f'{symbol}： {item[0]} < 60, 此后上涨 {item[1]} 个交易日。')
    #
    # df: pd.DataFrame = load_data('CZCE.PF105', QWPeriod(1, QWPeriodUnitType.Hour))
    # x = wave(df.loc['2020-10-23 21:00:00':'2020-10-23 22:59:00'])
    # print(x)


if __name__ == '__main__':
    symbol_list = [
        'SHFE.au',
    ]
    period_list = [
        QWPeriod(1, QWPeriodUnitType.Day)
    ]

    for symbol in symbol_list:
        for period in period_list:
            test_wave_trend(symbol, period)

    # Test <get_holiday_list>
    # holiday_list = get_holiday_list()
    # for holiday in holiday_list:
    #     print(holiday)
    # print(expand_day_range(holiday_list[0]))
    # print(expand_day_range(holiday_list[13]))
    #
    # print(is_trading_day(date(2020, 10, 7)))
    # print(is_holiday(date(2020, 10, 7)))
    #
    # print(next_trading_day(date(2020, 10, 5)))
    #
    # for x in shrink_day_range([date(2020, 10, 9),
    #                            date(2020, 10, 12),
    #                            date(2020, 10, 13),
    #                            date(2020, 10, 14),
    #                            date(2020, 10, 16),
    #                            date(2020, 10, 19),
    #                            date(2020, 10, 21),
    #                            date(2020, 10, 23), ]):
    #     print(x)
