# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List
import os
from enum import Enum

import pandas as pd
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from talib import ATR

from QuantWorkshop.config import CONFIGS
from QuantWorkshop.utility import packages_path_str


class QWPivotPointType(Enum):
    NotPivot: 'NotPivot'
    Low: 'Low'
    High: 'High'


class QWPivotPoint(object):
    index: int
    label: pd.Timestamp
    type_: QWPivotPointType
    value: float

    def __init__(self, type_: QWPivotPointType, value: float, index: int, label: pd.Timestamp):
        self.type_ = type_
        self.value = value
        self.index = index
        self.label = label


def initial_zigzag(df: pd.DataFrame) -> tuple:
    high_initial: float = df.iloc[0]['high']
    low_initial: float = df.iloc[0]['low']

    high_current: float = df.iloc[1]['high']
    low_current: float = df.iloc[1]['low']

    high_preview: float
    low_preview: float

    if high_current >= high_initial and low_current >= low_initial:
        return df.index[0], low_initial, -1
    elif high_current <= high_initial and low_current <= low_initial:
        return df.index[0], high_initial, 1


# def zigzag_hl(df: pd.DataFrame, depth: int = 12, deviation: int = 5, backstep: int = 3):
#     """
#     Zigzag on High/Low.
#     :param df:
#     :param depth:
#     :param deviation:
#     :param backstep:
#     :return:
#     """
#     idx: int
#     highest: float
#     lowest: float
#     pivot_point_list: List[QWPivotPoint]
#
#     if 'zigzag' in df.columns:
#         print('not new')
#     else:
#         print('Column "zigzag_hl" not found. Calculate the entire series.')
#         # highest = df.iloc[0]['high']
#         # lowest = df.iloc[0]['low']
#
#         # 计算从 0 到 Depth-1 范围内的最高、最低点
#         df_cal: pd.DataFrame = df.iloc[0:depth]
#
#         highest = df_cal['high'].max()
#         pivot_high: QWPivotPoint = QWPivotPoint(
#             type_=QWPivotPointType.High,
#             value=highest,
#             label=df_cal[(df_cal.high == highest)].index.tolist()[-1],
#             index=df_cal.index.get_loc(df_cal[(df_cal.high == highest)].index.tolist()[-1])
#         )
#
#         lowest: float = df_cal['low'].min()
#         label_lowest: pd.Timestamp = df_cal[(df_cal.low == lowest)].index.tolist()[-1]
#         index_lowest: int = df_cal.index.get_loc(label_lowest)
#
#         print(f'high={highest}, index={label_highest} and at {index_highest}')
#         print(f'low={lowest}, index={label_lowest} and at {index_lowest}')
#
#         print(type(label_lowest))
#         # for idx in range(depth, len(df)):
#         #     if df.iloc[idx]['high']


def zigzag(df: pd.DataFrame, depth: int = 12, deviation: int = 5, backstep: int = 3):
    """
    锯齿趋势线。

    参数：
        Depth: int = 12
        Deviation: int = 5
        Backstep: int = 3

    算法：
    1) 对计算位置进行初期化
        1.1) 判断是否是第一次进行高低点计算，如果是，则设定计算位置为除去 Depth个图形最初的部分。
        1.2) 如果之前已经计算过，找到最近已知的三个拐点（高点或低点），将计算位置设置为倒数第三个拐点之后，重新计算最后的拐点。
    2) 从<步骤1>已经设置好的计算位置开始，将对用于存储高低点的变量进行初始化，准备计算高低点
        2.1) 计算 Depth 区间内的低点，如果该低点是当前低点，则进行2.1.1的计算，并将其记录成一个低点。
            2.1.1) 如果当前低点比上一个低点值小于相对点差(Deviation)；并且之前 Backstep 个 Bars 的记录的中，高于当前低点的值清空。
        2.2) 高点的计算如同 <2.1> 以及分支处理 <2.1.1>。
    3) 从<步骤1>已经设置好的计算位置开始，定义指标高点和低点
        3.1) 如果开始位置为高点，则接下来寻找低点，在找到低点之后，将下一个寻找目标定义为高点
        3.2) 如果开始位置为低点，则与<3.1>反之。

    以上可能比较难以理解，我们这边举个例子说明。假设上次计算的结果如下：
        倒数第14个Bar出现了一个高点(3.1)，倒数第4个是低点(1.5)，倒数第1个是新的高点(2.1)——因为距离倒数第14已经大于 Depth(14-1>12)。
        Bar-14 Bar-4 Bar-1 Bar-Current 高(3.1) 低(1.5) 高(2.1) X 对于 Bar-Current，即当前的价格X，

        CaseI.
        如果 X >= 2.1 + Deviation，则根据Zigzag的定义，这将是一个新的高点。
        假设这里 X = 2.3，那么我们绘制指标的时候应该成为： Bar-14 Bar-4 Bar-Current 高(3.1) 低(1.5) 高(2.3)

        CaseII.
        如果 1.5 - Deviation < X < 2.1 + Deviation，则我们继续等待价格的变化，所绘制的指标也不会变化。

        CaseIII.
        如果 X <= 1.5 - Deviation，则这是一个新的低点。
        假设这里 X=1.3，则我们绘制指标的时候应该成为： Bar-14 Bar-Current 高(3.1) 低(1.3)
        这个时候，之前的Bar-4因为在我们定义的 Backstep之内(1-4)，所以他的最低值会被清空， 根据算法第三步的定义，
        我们会一直寻找低点直到发现Bar-Current，这时候已经遍历过Bar-1，所以Bar-1定义的高点也不再成为拐点。
    """

    highest: float
    lowest: float
    if 'zigzag' in df.columns:
        print('not new')
    else:
        print('new')
        # 计算 Depth 范围内的最高、最低点
        df_cal = df.iloc[0:depth]
        print(df_cal)

        highest = df_cal['high'].max()
        idx_highest = df_cal[(df_cal.high == highest)].index.tolist()[-1]

        lowest = df_cal['low'].min()
        idx_lowest = df_cal[(df_cal.low == lowest)].index.tolist()[-1]

        print(f'high={highest}, index={idx_highest} and at {df_cal.index.get_loc(idx_highest)}')
        print(f'low={lowest}, index={idx_lowest} and at {df_cal.index.get_loc(idx_lowest)}')
        # print(df.head(depth * 2))

    # df_cal: pd.DataFrame = df.loc['2020-10-19 09:00:00':'2020-10-19 11:00:00']

    # Create zigzag trend line.
    ########################################
    # Find peaks(max).
    data_x: np.ndarray = df.index.values
    data_y: np.ndarray = df['close'].values
    peak_indexes = signal.argrelextrema(data_y, np.greater)
    peak_indexes = peak_indexes[0]

    # Find valleys(min).
    valley_indexes = signal.argrelextrema(data_y, np.less)
    valley_indexes = valley_indexes[0]

    # Merge peaks and valleys data points using pandas.
    df_peaks = pd.DataFrame({'date': data_x[peak_indexes], 'zigzag_y': data_y[peak_indexes]})
    df_valleys = pd.DataFrame({'date': data_x[valley_indexes], 'zigzag_y': data_y[valley_indexes]})
    df_peaks_valleys = pd.concat([df_peaks, df_valleys], axis=0, ignore_index=True, sort=True)

    # Sort peak and valley data points by date.
    df_peaks_valleys = df_peaks_valleys.sort_values(by=['date'])

    # Instantiate axes.
    (fig, ax) = plt.subplots(figsize=(10, 3))

    # Plot zigzag trend line.
    ax.plot(df_peaks_valleys['date'].values, df_peaks_valleys['zigzag_y'].values,
            color='red', label="zigzag")

    # Plot close price line.
    ax.plot(data_x, data_y, linestyle='dashed', color='black', label="Close Price", linewidth=1)

    # Customize graph.
    ##########################
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'ZigZag trend line')
    # plt.title(f'ZigZag trend line - {symbol} on {period.to_english()}')

    # Format time.
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    plt.gcf().autofmt_xdate()  # Beautify the x-labels
    plt.autoscale(tight=True)

    plt.legend(loc='best')
    plt.grid(True, linestyle='dashed')

    # Save graph to file.
    picture_directory: str = os.path.join(packages_path_str, CONFIGS['picture_path'])
    if not os.path.exists(picture_directory):
        os.mkdir(picture_directory)
    plt.savefig(os.path.join(picture_directory, 'zigzag.png'))


PEAK = 1
VALLEY = -1


def identify_initial_pivot(series: List[float], threshold_up: float, threshold_down: float) -> int:
    x_0: float = series[0]
    x_t: float = x_0

    max_x: float = x_0
    min_x: float = x_0

    max_t: int = 0
    min_t: int = 0

    threshold_up += 1
    threshold_down += 1

    for t in range(1, len(series)):
        x_t = series[t]

        if x_t / min_x >= threshold_up:
            return VALLEY if min_t == 0 else PEAK

        if x_t / max_x <= threshold_down:
            return PEAK if max_t == 0 else VALLEY

        if x_t > max_x:
            max_x = x_t
            max_t = t

        if x_t < min_x:
            min_x = x_t
            min_t = t

    t_n = len(series) - 1
    return VALLEY if x_0 < series[t_n] else PEAK


def peak_valley_pivots(series: List[float], threshold_up: float, threshold_down: float):
    """
    Find the peaks and valleys of a series.
    :param series: the series to analyze
    :param threshold_up: minimum relative change necessary to define a peak
    :param threshold_down: minimum relative change necessary to define a valley
    :return: an array with 0 indicating no pivot and -1 and 1 indicating
        valley and peak
    The First and Last Elements
    ---------------------------
    The first and last elements are guaranteed to be annotated as peak or
    valley even if the segments formed do not have the necessary relative
    changes. This is a tradeoff between technical correctness and the
    propensity to make mistakes in data analysis. The possible mistake is
    ignoring data outside the fully realized segments, which may bias
    analysis.
    """
    if threshold_down > 0:
        raise ValueError('The down_thresh must be negative.')

    initial_pivot: int = identify_initial_pivot(series, threshold_up, threshold_down)
    t_n: int = len(series)
    pivots: np.ndarray = np.zeros(t_n, dtype=np.int_)
    trend: int = -initial_pivot
    last_pivot_t: int = 0
    last_pivot_x: float = series[0]
    x: float
    r: float

    pivots[0] = initial_pivot

    # Adding one to the relative change thresholds saves operations. Instead
    # of computing relative change at each point as x_j / x_i - 1, it is
    # computed as x_j / x_1. Then, this value is compared to the threshold + 1.
    # This saves (t_n - 1) subtractions.
    threshold_up += 1
    threshold_down += 1

    for t in range(1, t_n):
        x = series[t]
        r = x / last_pivot_x

        if trend == -1:
            if r >= threshold_up:
                pivots[last_pivot_t] = trend
                trend = PEAK
                last_pivot_x = x
                last_pivot_t = t
            elif x < last_pivot_x:
                last_pivot_x = x
                last_pivot_t = t
        else:
            if r <= threshold_down:
                pivots[last_pivot_t] = trend
                trend = VALLEY
                last_pivot_x = x
                last_pivot_t = t
            elif x > last_pivot_x:
                last_pivot_x = x
                last_pivot_t = t

    if last_pivot_t == t_n-1:
        pivots[last_pivot_t] = trend
    elif pivots[t_n-1] == 0:
        pivots[t_n-1] = -trend

    return pivots


def max_drawdown(series: np.ndarray) -> float:
    """
    Compute the maximum drawdown of some sequence.
    :return: 0 if the sequence is strictly increasing.
        otherwise the abs value of the maximum drawdown
        of sequence X
    """
    mdd: float = 0
    peak: float = series[0]
    x: float
    dd: float

    for x in series:
        if x > peak:
            peak = x

        dd = (peak - x) / peak

        if dd > mdd:
            mdd = dd

    return mdd if mdd != 0.0 else 0.0


def pivots_to_modes(pivots: List[int]):
    """
    Translate pivots into trend modes.
    :param pivots: the result of calling ``peak_valley_pivots``
    :return: numpy array of trend modes. That is, between (VALLEY, PEAK] it
    is 1 and between (PEAK, VALLEY] it is -1.
    """

    x: int
    t: int
    modes: np.ndarray = np.zeros(len(pivots), dtype=np.int_)
    mode: int = -pivots[0]

    modes[0] = pivots[0]

    for t in range(1, len(pivots)):
        x = pivots[t]
        if x != 0:
            modes[t] = mode
            mode = -x
        else:
            modes[t] = mode

    return modes


def compute_segment_returns(X, pivots):
    """
    :return: numpy array of the pivot-to-pivot returns for each segment."""
    pivot_points = X[pivots != 0]
    return pivot_points[1:] / pivot_points[:-1] - 1.0


class Trend(Enum):
    Up = 'UP'
    Down = 'DOWN'
    Sideways = 'Sideways'


def zigzag_hl(df: pd.DataFrame, echo: bool = False) -> tuple:
    """
    用最高价和最低价做趋势判断。

    返回一个列表，表中每个元素均为三个字段的元组。
    三个字段依次为：趋势开始的K线index, 趋势结束的K线index, 趋势。
    :return:  List[Tuple[int, int, Trend]]
    """

    message = '第 {index} 个数据, ' \
              '最高价/前最高价: {high} / {prev_high}, Delta = {dh}, ' \
              '最低价/前最低价: {low} / {prev_low}, Delta = {dl}, ' \
              '趋势: {trend}, {status}.'

    pivot_point_list: list = [(df.index[0], df.iloc[0]['low'])]
    high_list: list = []
    low_list: list = [(df.index[0], df.iloc[0]['low'])]
    cursor: float = df.iloc[0]['low']
    trend: Trend = Trend.Up

    index: int

    for index in range(1, len(df.index)):
        if trend == Trend.Up:
            if df.iloc[index]['high'] >= cursor:
                status = '延续'
                cursor = df.iloc[index]['high']
            else:
                status = '转折'
                pivot_point_list.append((df.index[index - 1], df.iloc[index - 1]['high']))
                if len(high_list) >= 2 and len(low_list) >= 2 and \
                        high_list[-1][1] <= df.iloc[index - 1]['high'] <= high_list[-2][1]:
                    del high_list[-1]
                    del low_list[-1]
                high_list.append((df.index[index - 1], df.iloc[index - 1]['high']))
                cursor = df.iloc[index]['low']
                trend = Trend.Down
        else:
            if df.iloc[index]['low'] <= cursor:
                status = '延续'
                cursor = df.iloc[index]['low']
            else:
                status = '转折'
                pivot_point_list.append((df.index[index - 1], df.iloc[index - 1]['low']))
                if len(high_list) >= 2 and len(low_list) >= 2 and \
                        low_list[-2][1] <= df.iloc[index - 1]['low'] <= low_list[-1][1]:
                    del high_list[-1]
                    del low_list[-1]
                low_list.append((df.index[index - 1], df.iloc[index - 1]['low']))
                cursor = df.iloc[index]['high']
                trend = Trend.Up

        if echo:
            print(message.format(index=index,
                                 high=df.iloc[index]['high'],
                                 prev_high=df.iloc[index - 1]['high'],
                                 dh=df.iloc[index]['high'] - df.iloc[index - 1]['high'],
                                 low=df.iloc[index]['low'],
                                 prev_low=df.iloc[index - 1]['low'],
                                 dl=df.iloc[index]['low'] - df.iloc[index - 1]['low'],
                                 trend=trend.value,
                                 status=status
                                 )
                  )

    hl_list: list = low_list + high_list
    hl_list.sort(key=lambda x: x[0])
    return pivot_point_list, hl_list
