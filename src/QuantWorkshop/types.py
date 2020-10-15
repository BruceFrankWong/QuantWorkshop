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

    def to_second(self) -> int:
        if self.value == 'Tick':
            return 0
        elif self.value == 'Second':
            return 1
        elif self.value == 'Minute':
            return 60
        elif self.value == 'Hour':
            return 60 * 60
        elif self.value == 'Day':
            return 60 * 60 * 24
        elif self.value == 'Week':
            return 60 * 60 * 24 * 5
        elif self.value == 'Month':
            return 60 * 60 * 24 * 5 * 4
        elif self.value == 'Year':
            return 60 * 60 * 24 * 5 * 4 * 12

    def to_chinese(self) -> str:
        if self.value == 'Tick':
            return 'Tick'
        elif self.value == 'Second':
            return '秒'
        elif self.value == 'Minute':
            return '分钟'
        elif self.value == 'Hour':
            return '小时'
        elif self.value == 'Day':
            return '日'
        elif self.value == 'Week':
            return '周'
        elif self.value == 'Month':
            return '月'
        elif self.value == 'Year':
            return '年'


class QWPeriod(object):
    unit: QWPeriodUnitType
    frequency: int

    def __init__(self, frequency: int, unit: QWPeriodUnitType):
        self.unit = unit
        if frequency < 1:
            raise ValueError('parameter <frequency> should be a positive integer.')
        else:
            self.frequency = frequency

    def to_second(self) -> int:
        return self.frequency * self.unit.to_second()

    def to_english(self) -> str:
        return f'{str(self.frequency) if self.frequency > 1 else ""}{self.unit.value}'

    def to_chinese(self) -> str:
        return f'{str(self.frequency) if self.frequency > 1 else ""}{self.unit.to_chinese()}'

    def __repr__(self) -> str:
        return f'<QWPeriod(frequency={self.frequency}), unit={self.unit.value}>'

    def __str__(self) -> str:
        result: str = ''
        if self.frequency > 1:
            result += str(self.frequency)
        result += self.unit.value
        return result


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
