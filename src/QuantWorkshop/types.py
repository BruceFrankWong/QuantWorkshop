# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


"""
QuantWorkshop - types define module.
"""


from enum import Enum


class TQRunningMode(Enum):
    """
    天勤量化你的运行模式。
    """
    BacktestMode = 'Backtest'   # 回测模式
    ReplayMode = 'Replay'       # 重放模式
    SimulateMode = 'Simulate'   # 模拟模式
    RealMode = 'Real'           # 实盘模式


class QWDirectionType(Enum):
    """
    买卖方向。
    """
    Buy = 'BUY'
    Long = 'BUY'
    Ask = 'BUY'
    Sell = 'SELL'
    Short = 'SELL'
    Bid = 'SELL'


class QWOffsetType(Enum):
    """
    开平标记。
    """
    Open = 'OPEN'               # 开
    Close = 'CLOSE'             # 平
    CloseToday = 'CLOSETODAY'   # 平今


class QWOrderStatus(Enum):
    Alive = 'ALIVE'
    Finished = 'FINISHED'
    Canceled = 'CANCELED'


class QWPeriodUnitType(Enum):
    Tick = 'Tick'
    Second = 'Second'
    Minute = 'Minute'
    Hour = 'Hour'
    Day = 'Day'
    Week = 'Week'
    Month = 'Month'
    Year = 'Year'


class QWPeriod(object):
    unit: QWPeriodUnitType
    frequency: int

    def __init__(self, **kwargs):
        pass

    def to_second(self) -> int:
        if self.unit == QWPeriodUnitType.Tick:
            return 0
        elif self.unit == QWPeriodUnitType.Second:
            return self.frequency
        elif self.unit == QWPeriodUnitType.Minute:
            return self.frequency * 60
        elif self.unit == QWPeriodUnitType.Hour:
            return self.frequency * 60 * 60
        elif self.unit == QWPeriodUnitType.Day:
            return self.frequency * 60 * 60 * 24
        elif self.unit == QWPeriodUnitType.Week:
            return self.frequency * 60 * 60 * 24 * 5
        elif self.unit == QWPeriodUnitType.Month:
            return self.frequency * 60 * 60 * 24 * 20
        elif self.unit == QWPeriodUnitType.Year:
            return self.frequency * 60 * 60 * 24 * 240
        else:
            raise RuntimeError('<unit> is unknown type.')

    @classmethod
    def period_unit_to_second(cls, pu: QWPeriodUnitType) -> int:
        if pu == QWPeriodUnitType.Tick:
            return 0
        elif pu == QWPeriodUnitType.Second:
            return 1
        elif pu == QWPeriodUnitType.Minute:
            return 60
        elif pu == QWPeriodUnitType.Hour:
            return 60 * 60
        elif pu == QWPeriodUnitType.Day:
            return 60 * 60 * 24


class QWExchange(Enum):
    """
    交易所
    """
    SSE = 'SSE'         # 上交所
    SZSE = 'SZSE'       # 深交所
    SHFE = 'SHFE'       # 上期所
    DCE = 'DCE'         # 大商所
    CZCE = 'CZCE'       # 郑商所
    CFFEX = 'CFFEX'     # 中金所
    INE = 'INE'         # 上能所
    HKEX = 'HKEX'       # 港交所
