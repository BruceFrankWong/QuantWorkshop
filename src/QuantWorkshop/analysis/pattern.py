# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from QuantWorkshop.model.bar import BarType, FuturesBar


def is_engulfing(bar_prev: FuturesBar, bar_next: FuturesBar) -> bool:
    """
    反包。
    :return:
    """
    key_price: float
    if bar_prev.price_close > bar_prev.price_open:
        key_price = bar_prev.price_low
    else:
        key_price = bar_prev.price_high

    # 前后两根K线方向相同
    if bar_next.type_ == bar_prev.type_:
        return False
    if bar_prev.type_ == BarType.Bullish:
        if min(bar_next.price_open, bar_next.price_close, bar_next.price_low) <= bar_prev.price_low:
            return True
        else:
            return False
    elif bar_prev.type_ == BarType.Bearish:
        if max(bar_next.price_open, bar_next.price_close, bar_next.price_high) >= bar_prev.price_high:
            return True
        else:
            return False


def is_c_point(pubu: float, bar_prev: FuturesBar, bar: FuturesBar, bar_next: FuturesBar) -> bool:
    pass
