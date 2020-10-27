# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from datetime import date, timedelta

import pandas as pd

from QuantWorkshop.types import QWPeriod, QWPeriodUnitType
from QuantWorkshop.analysis import load_data
from QuantWorkshop.analysis.indicator import wave


def is_consecutive(day_1: date, day_2: date) -> bool:
    if day_1 > day_2:
        day_1, day_2 = day_2, day_1
    if 1 <= day_1.isoweekday() <= 4:
        if day_1 + timedelta(days=1) == day_2:
            return True
        else:
            return False
    else:
        if day_1 + timedelta(days=2) == day_2:
            return True
        else:
            return False


if __name__ == '__main__':
    symbol_list = [
        'SHFE.au',
    ]
    period_list = [
        QWPeriod(1, QWPeriodUnitType.Day)
    ]

    wave_low_index: list = []
    wave_low_date: list = []
    wave_high_index: list = []
    wave_high_date: list = []
    result_low: list = []
    for symbol in symbol_list:
        for period in period_list:
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
            print(f'{symbol}：自 {df.index[0].date()} 至 {df.index[-1].date()}，共 {len(df)} 个交易日。'
                  f'低于 60 的日期共有 {len(wave_low_index)} 个，占比{len(wave_low_index) / len(df) * 100:.3f}%；'
                  f'高于 170 的日期共有 {len(wave_high_index)} 个，占比{len(wave_high_index) / len(df) * 100:.3f}%。')

            print(wave_low_date)
            print(wave_high_date)

            # 消除连续
            wave_low_filtered = []
            for idx in range(1, len(wave_low_index)):
                if is_consecutive(wave_low_date[idx - 1], wave_low_date[idx]):
                    j = 0
                    while is_consecutive(wave_low_date[idx-1], wave_low_date[idx+j]):
                        j += 1
                    wave_low_filtered.append((idx-1, idx+j))
                else:
                    wave_low_filtered.append((idx,))

            idx: int = 1
            while idx < len(wave_low_date):
                if is_consecutive(wave_low_date[idx - 1], wave_low_date[idx]):
                    j = idx - 1
                    while is_consecutive(wave_low_date[idx-1], wave_low_date[idx+j]):
                        j += 1
                else:
                    wave_low_filtered.append((idx,))
                    idx += 1
            for item in wave_low_filtered:
                print(item)
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

    # df: pd.DataFrame = load_data('CZCE.PF105', QWPeriod(1, QWPeriodUnitType.Hour))
    # x = wave(df.loc['2020-10-23 21:00:00':'2020-10-23 22:59:00'])
    # print(x)
