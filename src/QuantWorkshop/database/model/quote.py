# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List
from datetime import date

from sqlalchemy import Table, Column, ForeignKey, String, Integer, Float, Date, Time, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from ..interface import ModelBase, db_session
from .exchange import Exchange


class QuoteBase(ModelBase):
    """
    行情的基类。
    """
    __abstract__ = True
    __tablename__ = 'quote_base'

    id = Column(Integer, primary_key=True)
    price_open = Column(Float, nullable=False)      # 开盘价
    price_high = Column(Float, nullable=False)      # 最高价
    price_low = Column(Float, nullable=False)       # 最低价
    price_close = Column(Float, nullable=False)     # 收盘价
    volume = Column(Integer, nullable=False)        # 成交量
    amount = Column(Float, nullable=False)          # 成交额

    def __repr__(self):
        return f'QuoteBase(' \
               f'open={self.price_open}, ' \
               f'high={self.price_high}, ' \
               f'low={self.price_low}, ' \
               f'close={self.price_close}, ' \
               f'volume={self.volume}, ' \
               f'amount={self.amount})'


class QuoteDailyBase(QuoteBase):
    """
    日线行情的基类。
    """
    __abstract__ = True
    __tablename__ = 'quote_daily'

    date = Column(Date, nullable=False)

    def __repr__(self):
        return f'QuoteBase(' \
               f'date={self.date}, ' \
               f'open={self.price_open}, ' \
               f'high={self.price_high}, ' \
               f'low={self.price_low}, ' \
               f'close={self.price_close}, ' \
               f'volume={self.volume}, ' \
               f'amount={self.amount})'


class QuoteMinuteBase(QuoteBase):
    """
    分钟行情的基类。
    """
    __abstract__ = True
    __tablename__ = 'quote_minutely'

    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    def __repr__(self):
        return f'QuoteBase(' \
               f'date={self.date}, ' \
               f'time={self.time}, ' \
               f'open={self.price_open}, ' \
               f'high={self.price_high}, ' \
               f'low={self.price_low}, ' \
               f'close={self.price_close}, ' \
               f'volume={self.volume}, ' \
               f'amount={self.amount})'


quote_daily_table = Table(
    'quote_daily',
    ModelBase.metadata,
    Column('id', Integer, primary_key=True),
    Column('keyword_id', Integer, ForeignKey("keyword.id"),
           primary_key=True)
)
