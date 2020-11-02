# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import pandas as pd
import talib


def band_artifact(df: pd.DataFrame, n_rsi_1: int = 6, n_rsi_2: int = 12, n_wr: int = 14) -> pd.DataFrame:
    # RSI 部分。
    df['rsi_1'] = talib.RSI(df['close'], n_rsi_1)
    df['rsi_2'] = talib.RSI(df['close'], n_rsi_2)

    # WR 部分。
    df['wr'] = talib.WILLR(df['high'], df['low'], df['close'], n_wr)

    # 波段神器。
    # df['ba'] = 100 + df['wr'] + df['rsi_max']
    df['ba'] = 100 + df['wr'] + df[['rsi_1', 'rsi_2']].max(axis=1)
    return df
