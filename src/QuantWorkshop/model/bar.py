# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from enum import Enum


class BarType(Enum):
    Black = 'Bullish'
    White = 'Bearish'
    Bullish = 'Bullish'
    Bearish = 'Bearish'
    Doji = 'Doji'


class BarBase(object):
    """
    行情的基类。
    """
    price_open: float   # 开盘价
    price_high: float   # 最高价
    price_low: float    # 最低价
    price_close: float  # 收盘价
    volume: int         # 成交量
    amount: float       # 成交额

    def __init__(self,
                 price_open: float,
                 price_high: float,
                 price_low: float,
                 price_close: float,
                 volume: int,
                 amount: float):
        self.price_open = price_open
        self.price_high = price_high
        self.price_low = price_low
        self.price_close = price_close
        self.volume = volume
        self.amount = amount

    @property
    def type_(self) -> BarType:
        if self.price_close == self.price_open:
            return BarType.Doji
        elif self.price_close == self.price_open:
            return BarType.Bullish
        else:
            return BarType.Bearish

    def __repr__(self):
        return f'BarBase(' \
               f'open={self.price_open}, ' \
               f'high={self.price_high}, ' \
               f'low={self.price_low}, ' \
               f'close={self.price_close}, ' \
               f'volume={self.volume}, ' \
               f'amount={self.amount})'


class FuturesBar(BarBase):
    """
    期货行情。
    """
    open_oi: int
    close_oi: int
    settle: float

    def __init__(self,
                 price_open: float,
                 price_high: float,
                 price_low: float,
                 price_close: float,
                 volume: int,
                 amount: float,
                 open_oi: int,
                 close_oi: int,
                 settle: float):
        super().__init__(price_open, price_high, price_low, price_close, volume, amount)
        self.open_oi = open_oi
        self.close_oi = close_oi
        self.settle = settle

    def __repr__(self):
        return f'FuturesBar(' \
               f'open={self.price_open}, ' \
               f'high={self.price_high}, ' \
               f'low={self.price_low}, ' \
               f'close={self.price_close}, ' \
               f'volume={self.volume}, ' \
               f'amount={self.amount}), ' \
               f'open_oi={self.open_oi}, ' \
               f'close_oi={self.close_oi}, ' \
               f'settle={self.settle}, )' \
