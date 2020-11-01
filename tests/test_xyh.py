# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List, Tuple, Union
import os
import csv
from datetime import date, timedelta

import pandas as pd
from openpyxl import Workbook

from QuantWorkshop.utility import packages_path_str
from QuantWorkshop.types import QWPeriod, QWPeriodUnitType
from QuantWorkshop.analysis import load_data
from QuantWorkshop.analysis.indicator import band_artifact


def get_df_label(df: pd.DataFrame, idx: int) -> str:
    return df.index[idx].strftime('%Y-%m-%d %H:%M:%S')


def get_df_index(df: pd.DataFrame, idx: Union[str, pd.Timestamp]) -> int:
    return df.index.get_loc(idx)


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


def group(data_list: List[int]) -> List[Tuple[int, int]]:
    result: List[Tuple[int, int]] = []
    first_consecutive: int = -1
    for idx in range(len(data_list) - 1):
        if data_list[idx] + 1 == data_list[idx+1]:
            if first_consecutive == -1:
                first_consecutive = data_list[idx]
        else:
            if first_consecutive == -1:
                result.append((data_list[idx], data_list[idx]))
            else:
                result.append((first_consecutive, data_list[idx]))
            first_consecutive = -1

    if first_consecutive != -1:
        result.append((data_list[-1], data_list[-1]))
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


# def is_engulfing(df: pd.DataFrame, bar_prev: int, bar_next: int) -> bool:
#     """
#     反包。
#     :return:
#     """
#     key_price: float
#     if bar_prev.price_close > bar_prev.price_open:
#         key_price = bar_prev.price_low
#     else:
#         key_price = bar_prev.price_high
#
#     # 前后两根K线方向相同
#     if bar_next.type_ == bar_prev.type_:
#         return False
#     if bar_prev.type_ == BarType.Bullish:
#         if min(bar_next.price_open, bar_next.price_close, bar_next.price_low) <= bar_prev.price_low:
#             return True
#         else:
#             return False
#     elif bar_prev.type_ == BarType.Bearish:
#         if max(bar_next.price_open, bar_next.price_close, bar_next.price_high) >= bar_prev.price_high:
#             return True
#         else:
#             return False


def test_band_artifact_low(df: pd.DataFrame, open_window: int = 5):
    # 源数据长度
    length: int = len(df)

    # 波段低点
    list_low_index: list = [df.index.get_loc(x) for x in df[df['ba'] <= 60].index]

    # 低点数量
    count_low_index: int = len(list_low_index)

    # 波段低点分组
    list_low_group: List[Tuple[int, int]] = group(list_low_index)
    dict_low: dict = {
        'begin': [x[0] for x in list_low_group],
        'end': [x[1] for x in list_low_group],
    }

    df_low: pd.DataFrame = pd.DataFrame(dict_low, dtype=int)
    df_low['length'] = df_low['end'] - df_low['begin']

    # 内存回收
    del list_low_index, list_low_group, dict_low

    # 其它column
    df_low['extreme_ba'] = 0        # 波段神器的极值
    df_low['extreme_high'] = 0      # 最高价的极值

    df_low['open_delta_ba'] = 0     # 按照波段神器最低值买入，开仓偏移多少个周期。
    df_low['close_delta_ba'] = 0    # 按照波段神器最低值买入，平仓偏移多少个周期。
    df_low['price_open_ba'] = 0     # 按照波段神器最低值买入，开仓价理论值。
    df_low['price_close_ba'] = 0    # 按照波段神器最低值买入，平仓价理论值。
    df_low['open_type_ba'] = 0      # 按照波段神器最低值买入，开仓类型。1=反包，2=连续阳线。

    df_low['open_delta_high'] = 0   # 按照区间最高价的最低值买入，开仓偏移多少个周期。
    df_low['close_delta_high'] = 0  # 按照区间最高价的最低值买入，平仓偏移多少个周期。
    df_low['price_open_high'] = 0   # 按照区间最高价的最低值买入，开仓价理论值。
    df_low['price_close_high'] = 0  # 按照区间最高价的最低值买入，平仓价理论值。
    df_low['open_type_high'] = 0    # 按照区间最高价的最低值买入，开仓类型。1=反包，2=连续阳线。

    df_low['delta_ba_and_high'] = 0     # 区间最高价的最低值比波段神器极值点延后多少个周期。

    # 找出极值
    for idx in range(len(df_low)):
        if df_low.iloc[idx]['begin'] == df_low.iloc[idx]['end']:
            df_low.loc[idx, 'extreme_ba'] = df_low.loc[idx, 'begin']
            df_low.loc[idx, 'extreme_high'] = df_low.loc[idx, 'begin']
        else:
            extreme_ba = df.iloc[df_low.iloc[idx]['begin']:df_low.iloc[idx]['end']]['ba'].min()
            df_low.loc[idx, 'extreme_ba'] = df.index.get_loc(df[df['ba'] == extreme_ba].index[0])

            extreme_high = df.iloc[df_low.iloc[idx]['begin']:df_low.iloc[idx]['end']]['high'].min()
            possible_index_list = df[df['high'] == extreme_high].index
            if len(possible_index_list) == 1:
                df_low.loc[idx, 'extreme_high'] = df.index.get_loc(possible_index_list[0])
            else:
                date_begin = df.index[df_low.iloc[idx]['begin']].date()
                date_end = df.index[df_low.iloc[idx]['end']].date()
                for dt_stamp in possible_index_list:
                    if date_begin <= dt_stamp.date() <= date_end:
                        df_low.loc[idx, 'extreme_high'] = df.index.get_loc(dt_stamp)

    df_low['delta_ba_and_high'] = df_low['extreme_high'] - df_low['extreme_ba']

    # 计算开仓条件
    for idx in range(len(df_low)):
        # 底部，期待反弹
        # 买入点：反包或连续阳线

        # 按照波段神器最低值买入
        idx_df = df_low.loc[idx, 'extreme_ba']

        # 底部后第n天反包
        for n in range(1, open_window + 1):
            if df.iloc[idx_df + n]['high'] > df.iloc[idx_df]['high']:
                df_low.loc[idx, 'open_type_ba'] = n      # 开仓条件为反包
                df_low.loc[idx, 'open_delta_ba'] = n     # 开仓时间为波段神器极值之后的第1天
                df_low.loc[idx, 'price_open_ba'] = df.iloc[idx_df]['high']   # 开仓价为波段神器极值的当天的最高价
                break
            elif n >= 2 and \
                 df.iloc[idx_df + n]['close'] > df.iloc[idx_df + n]['open'] and \
                 df.iloc[idx_df + n - 1]['close'] > df.iloc[idx_df + n - 1]['open']:
                df_low.loc[idx, 'open_type_ba'] = 2
                df_low.loc[idx, 'open_delta_ba'] = n + 1
                df_low.loc[idx, 'price_open_ba'] = df.iloc[idx_df + n + 1]['open']
                break
        if df_low.loc[idx, 'open_delta_ba'] == 0:
            df_low.loc[idx, 'open_delta_ba'] = -1
            df_low.loc[idx, 'open_type_ba'] = -1
            df_low.loc[idx, 'price_open_ba'] = -1

        # 按照区间最高价的最低值买入
        idx_df = df_low.loc[idx, 'extreme_high']

        # 底部后第1天反包
        if df.iloc[idx_df + 1]['high'] > df.iloc[idx_df]['high']:
            df_low.loc[idx, 'open_delta_high'] = 1
            df_low.loc[idx, 'open_type_high'] = 1
        # 底部后第2天反包
        elif df.iloc[idx_df + 2]['high'] > df.iloc[idx_df]['high']:
            df_low.loc[idx, 'open_delta_high'] = 2
            df_low.loc[idx, 'open_type_high'] = 1
        # 底部后第3天反包
        elif df.iloc[idx_df + 3]['high'] > df.iloc[idx_df]['high']:
            df_low.loc[idx, 'open_delta_high'] = 3
            df_low.loc[idx, 'open_type_high'] = 1
        # 底部后第4天反包
        elif df.iloc[idx_df + 4]['high'] > df.iloc[idx_df]['high']:
            df_low.loc[idx, 'open_delta_high'] = 4
            df_low.loc[idx, 'open_type_high'] = 1
        # 底部后第5天反包
        elif df.iloc[idx_df + 5]['high'] > df.iloc[idx_df]['high']:
            df_low.loc[idx, 'open_delta_high'] = 5
            df_low.loc[idx, 'open_type_high'] = 1
        # 连续两天（第1天、第2天）阳线
        elif df.iloc[idx_df + 1]['close'] > df.iloc[idx_df + 1]['open'] and \
                df.iloc[idx_df + 2]['close'] > df.iloc[idx_df + 2]['open']:
            df_low.loc[idx, 'open_delta_high'] = 3
            df_low.loc[idx, 'open_type_high'] = 2
        # 连续两天（第2天、第3天）阳线
        elif df.iloc[idx_df + 2]['close'] > df.iloc[idx_df + 2]['open'] and \
                df.iloc[idx_df + 3]['close'] > df.iloc[idx_df + 3]['open']:
            df_low.loc[idx, 'open_delta_high'] = 4
            df_low.loc[idx, 'open_type_high'] = 2
        # 连续两天（第3天、第4天）阳线
        elif df.iloc[idx_df + 3]['close'] > df.iloc[idx_df + 3]['open'] and \
                df.iloc[idx_df + 4]['close'] > df.iloc[idx_df + 4]['open']:
            df_low.loc[idx, 'open_delta_high'] = 5
            df_low.loc[idx, 'open_type_high'] = 2
        else:
            df_low.loc[idx, 'open_delta_high'] = -1
            df_low.loc[idx, 'open_type_high'] = -1

    # wave_low_filtered_index: List[int] = []
    # for item in list_low_group:
    #     if item[0] == item[1]:
    #         wave_min = df.iloc[item[0]]['band_artifact']
    #     else:
    #         wave_min = df.iloc[item[0]:item[1]]['band_artifact'].min()
    #     label = df[df['band_artifact'] == wave_min].index
    #     print(f'在日期 {item[0]} 至 {item[1]} 的区间中，最低值出现在 {label[0].strftime("%Y-%m-%d")}，最低值 = {wave_min:.3f}。')
    #     # print(f'在日期 {item[0]} 至 {item[1]} 的区间中，'
    #     #       f'最低值出现在 {label.strftime("%Y-%m-%d")}'
    #     #       f'， 最低值 = {wave_min:.3f}。')
    #     wave_low_filtered_index.append(df.index.get_loc(label[0]))
    #
    # print('=' * 20)
    #
    # # 测试
    # column_list = ['close', 'high']
    # result_list: list = []
    # result_day: list
    # for idx in wave_low_filtered_index:
    #     # 底部，期待反弹
    #     # 买入点：反包或连续阳线
    #
    #     # 底部后第1天反包
    #     if df.iloc[idx + 1]['high'] > df.iloc[idx]['high']:
    #         trigger = 1
    #     # 底部后第2天反包
    #     elif df.iloc[idx + 2]['high'] > df.iloc[idx]['high']:
    #         trigger = 2
    #     # 连续两天阳线
    #     elif df.iloc[idx+1]['open'] > df.iloc[idx+1]['close'] and df.iloc[idx+2]['open'] > df.iloc[idx+2]['close']:
    #         trigger = 3
    #     else:
    #         trigger = -1
    #     close = df.iloc[idx]['close']
    #     flag: bool = False
    #     if df.iloc[idx]['close'] < df.iloc[idx+1]['close']:
    #         i: int = 1
    #         while df.iloc[idx]['close'] < df.iloc[idx+i]['close'] and idx+i < len(df) - 1:
    #             i += 1
    #         result_list.append((df.index[idx], i))
    #     else:
    #         result_list.append((df.index[idx], -1))
    # for item in result_list:
    #     print(f'{item[0]} < 60, 此后上涨 {item[1]} 个交易日。')
    #
    # df: pd.DataFrame = load_data('CZCE.PF105', QWPeriod(1, QWPeriodUnitType.Hour))
    # x = wave(df.loc['2020-10-23 21:00:00':'2020-10-23 22:59:00'])

    print('=' * 20)

    print(
        f'自 {df.index[0].date()} 至 {df.index[-1].date()}，共 {len(df)} 个交易日。'
        f'波段神器低于 60的日期共有{count_low_index}个，占比{count_low_index/length*100:.3f}%，分为{len(df_low)}段。'
    )
    for idx in range(len(df_low)):
        print(f"{idx+1:3d}: "
              f"在 {df.index[df_low.loc[idx, 'begin']].strftime('%Y-%m-%d')}"
              f" 至 {df.index[df_low.loc[idx, 'end']].strftime('%Y-%m-%d')} 的区间中，"
              f"共{df_low.loc[idx, 'length']}个周期；"
              f"【波段神器】最低值 = {df.iloc[df_low.loc[idx, 'extreme_ba']]['ba']:.3f}，"
              f"出现在 {df.index[df_low.loc[idx, 'extreme_ba']].strftime('%Y-%m-%d')}，"
              f"【最高价】的最低值 = {df.iloc[df_low.loc[idx, 'extreme_high']]['high']:.3f}，"
              f"出现在 {df.index[df_low.loc[idx, 'extreme_high']].strftime('%Y-%m-%d')}；"
              f"最高价比波段神器延后 {df_low.loc[idx, 'delta_ba_and_high']:3d}个周期。"
              f"按照波段神器买入，时间在最低值之后{df_low.loc[idx, 'open_delta_ba']:3d}个周期；"
              f"按照最高价买入，时间在最低值之后{df_low.loc[idx, 'open_delta_high']:3d}个周期。")

    print('=' * 20)

    print(f"【波段神器】最低值买入时间出现了{len(df_low[df_low['open_delta_ba']>0]):2d}次，"
          f"占比{len(df_low[df_low['open_delta_ba']>0])/len(df_low)*100:.3f}%；"
          f"【区间最高价】最低值买入时间出现了{len(df_low[df_low['open_delta_high']>0]):2d}次，"
          f"占比{len(df_low[df_low['open_delta_high']>0])/len(df_low)*100:.3f}%。")

    print('=' * 20)

    print('【波段神器】最低值 和 【区间最高价】最低值 都没有开仓机会的情况：', end='')
    dt_stamp = df_low[(df_low['open_delta_ba'] < 0) & (df_low['open_delta_high'] < 0)]
    dt_stamp.index = range(len(dt_stamp))
    for idx in range(len(dt_stamp)):
        print(
            f"{idx+1:3d}:"
            f"在日期 {df.index[dt_stamp.loc[idx, 'begin']].strftime('%Y-%m-%d')}"
            f" 至 {df.index[dt_stamp.loc[idx, 'end']].strftime('%Y-%m-%d')} 的区间中"
        )
    print('=' * 20)

    wb = Workbook()


def test_band_artifact_high(df: pd.DataFrame):
    # 源数据长度
    length: int = len(df)

    # 波段高点
    list_high_index: list = [df.index.get_loc(x) for x in df[df['ba'] >= 170].index]
    # 高点数量
    count_high_index: int = len(list_high_index)
    # 波段高点分组
    list_high_group: List[Tuple[int, int]] = group(list_high_index)

    print(
        f'自 {df.index[0].date()} 至 {df.index[-1].date()}，共 {len(df)} 个交易日。'
        f'高于170的日期共有{count_high_index}个，占比{count_high_index / length * 100:.3f}%，分为{len(list_high_group)}段。'
    )


if __name__ == '__main__':
    symbol_list = [
        'SHFE.au',
    ]
    period_list = [
        QWPeriod(1, QWPeriodUnitType.Day)
    ]

    for symbol in symbol_list:
        for period in period_list:
            data: pd.DataFrame = load_data(f'KQ.m@{symbol}', period)

            # # 指标计算
            # data['rsi'] = talib.RSI(df['close'], n_rsi)
            #
            # # WR 部分。
            # data['wr'] = talib.WILLR(df['high'], df['low'], df['close'], n_wr)
            #
            # # 波段神器。
            # df['band_artifact'] = 100 + df['wr'] + df['rsi']
            band_artifact(data)
            print(f'{symbol} on {period.to_english()}：')
            test_band_artifact_low(data)
            test_band_artifact_high(data)

    # df: pd.DataFrame = load_data(f'KQ.m@SHFE.ag', QWPeriod(1, QWPeriodUnitType.Day))
    # x = get_dataframe_label(df, -1)
    # print(type(x), x)
    # x = get_dataframe_index(df, '2020-10-30 00:00:00')
    # print(type(x), x)

    # print(df.iloc[-1])

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
