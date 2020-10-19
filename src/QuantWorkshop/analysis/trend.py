# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List
import os
from datetime import date

import pandas as pd
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from talib import ATR

from QuantWorkshop.config import CONFIGS
from QuantWorkshop.utility import packages_path_str
from QuantWorkshop.types import QWPeriod, QWPeriodUnitType
from QuantWorkshop.download import download


def zigzag(symbol: str, period: QWPeriod):
    """
    锯齿趋势线。
    """
    # 读取数据。
    csv_file: str = os.path.join(packages_path_str, CONFIGS['data_downloaded'], f'{symbol}_{period.to_english()}.csv')
    if not os.path.exists(csv_file):
        download(symbol, period, date(2016, 1, 1))
    df_x: pd.DataFrame = pd.read_csv(csv_file, index_col='datetime', parse_dates=True)
    # df.DatetimeIndex = df['datetime']

    df: pd.DataFrame = df_x.loc['2020-10-19 09:00:00':'2020-10-19 11:00:00']

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
    plt.title(f'ZigZag trend line - {symbol} on {period.to_english()}')

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
