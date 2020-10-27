# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import pandas as pd
import talib


def wave(df: pd.DataFrame, n_rsi: int = 6, n_wr: int = 14) -> pd.DataFrame:
    # RSI 部分。
    df['rsi'] = talib.RSI(df['close'], n_rsi)

    # WR 部分。
    df['wr'] = talib.WILLR(df['high'], df['low'], df['close'], n_wr)

    # 波段神器。
    df['wave'] = 100 + df['wr'] + df['rsi']
    return df
