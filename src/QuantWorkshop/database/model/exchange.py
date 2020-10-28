# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List

from sqlalchemy import Table, Column, ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship

from ..interface import ModelBase, db_session


relationship_table_exchange_and_security = Table(
    'relationship_exchange_and_security',
    ModelBase.metadata,
    Column('exchange_id', Integer, ForeignKey('exchange.id'), primary_key=True),
    Column('security_id', Integer, ForeignKey('security.id'), primary_key=True)
)


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

    security_list = relationship('Security',
                                 secondary=relationship_table_exchange_and_security,
                                 back_populates='exchange_list'
                                 )
    # holiday_list = relationship('Holiday', back_populates='exchange')
    stock_list = relationship('Stock', back_populates='exchange')
    futures_list = relationship('Futures', back_populates='exchange')
    option_list = relationship('Option', back_populates='exchange')
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

    @staticmethod
    def symbol_list() -> List[str]:
        result: List[str] = []
        for symbol in db_session.query(Exchange.symbol).all():
            result += symbol
        return result

    @staticmethod
    def name_list() -> List[str]:
        result: List[str] = []
        for symbol in db_session.query(Exchange.name).all():
            result += symbol
        return result

    def __repr__(self):
        return f'<Exchange(name="{self.name}", symbol="{self.symbol}")>'


# class RelationshipExchangeAndSecurity(ModelBase):
#     __tablename__ = 'relationship_exchange_and_security'
#
#     exchange_id = Column(Integer, ForeignKey('exchange.id'), primary_key=True)
#     security_id = Column(Integer, ForeignKey('security.id'), primary_key=True)
#
#     exchange = relationship(Exchange,
#                             back_populates='exchange_and_security',
#                             # cascade='all, delete-orphan'
#                             )
#     # security = relationship('Security', back_populates='exchange_list')
#     security = relationship('Security')
#
#     def __repr__(self):
#         return f'Exchange-Security({self.exchange_id}-{self.security_id})'


class Security(ModelBase):
    """
    产品类型。
    """
    __tablename__ = 'security'

    id = Column(Integer, primary_key=True)
    name_en = Column(String, nullable=False, unique=True)
    name_zh = Column(String, nullable=False, unique=True)

    exchange_list = relationship('Exchange',
                                 secondary=relationship_table_exchange_and_security,
                                 back_populates='security_list'
                                 )

    def __repr__(self):
        return f'<Security(name_zh={self.name_zh}, name_en={self.name_en})>'
