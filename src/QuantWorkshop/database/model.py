# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List
from datetime import date

from sqlalchemy import Table, Column, ForeignKey, String, Integer, Float, Date, Time, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from .interface import ModelBase


class Exchange(ModelBase):
    """
    交易所。
    """
    __tablename__ = 'exchange'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    fullname_zh = Column(String, nullable=False, unique=True)
    fullname_en = Column(String, nullable=False, unique=True)

    product_list = association_proxy('exchange_and_product_type', 'keyword')
    # holiday_list = relationship('Holiday', back_populates='exchange')
    # stock_list = relationship('Stock', back_populates='exchange')
    # futures_list = relationship('Futures', back_populates='exchange')
    # option_list = relationship('Option', back_populates='exchange')
    #
    # def is_trading_day(self, day: date) -> bool:
    #     if 6 <= day.isoweekday() <= 7:
    #         return False
    #     for holiday in self.get_holiday_by_year(day.year):
    #         if holiday.begin <= day <= holiday.end:
    #             return False
    #     return False
    #
    # def get_holiday_by_year(self, year: int) -> list:
    #     if year <= 2000 or year > date.today().year:
    #         raise ValueError('Parameter <year> should be in [2001, Current Year]')
    #     return db_session.query(Holiday).filter(Holiday.exchange_id == self.id,
    #                                             Holiday.begin >= date(year, 1, 1),
    #                                             Holiday.begin <= date(year+1, 1, 1)
    #                                             ).all()

    def __repr__(self):
        return f'<Exchange(name={self.name}, fullname={self.fullname}, abbr={self.symbol})>'


class ProductType(ModelBase):
    """
    产品类型。
    """
    __tablename__ = 'product_type'

    id = Column(Integer, primary_key=True)
    product_type = Column(String, nullable=False, unique=True)
    product_type_zh = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f'<ProductType(name_zh={self.name_zh}, name_en={self.name_en})>'


class ExchangeAndProductType(ModelBase):
    __tablename__ = 'exchange_and_product_type'

    exchange_id = Column(Integer, ForeignKey('exchange.id'), primary_key=True)
    product_type_id = Column(Integer, ForeignKey('product_type.id'), primary_key=True)

    exchange = relationship(Exchange,
                            backref=backref('exchange_and_product_type',
                                            cascade='all, delete-orphan'
                                            )
                            )
    product_type = relationship('ProductType')

    def __repr__(self):
        return f'Exchange-ProductType({self.exchange_id}-{self.product_type_id})'


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
