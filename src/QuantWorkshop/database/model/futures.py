# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List
from datetime import date

from sqlalchemy import Table, Column, ForeignKey, String, Integer, Float, Date, Time, DateTime
from sqlalchemy.orm import relationship

from ..interface import ModelBase, db_session
from .exchange import Exchange


class Futures(ModelBase):
    __tablename__ = 'futures'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    symbol = Column(String, nullable=False, unique=True)
    contract_url = Column(String, nullable=False)
    margin = Column(Float, nullable=False)
    size = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    fluctuation = Column(Float, nullable=False)

    exchange_id = Column(Integer, ForeignKey('exchange.id'), nullable=False)

    exchange = relationship('Exchange', back_populates='stock_list')

    # contract_list = relationship('FuturesContract', back_populates='futures')
    # main_contract_list = relationship('FuturesMainContract', back_populates='futures')

    # @property
    # def trading_contracts(self) -> List[str]:
    #     return self.trading_contracts_at(date.today())
    #
    # def trading_contracts_at(self, day: date) -> List[str]:
    #     return db_session.query(FuturesContract).filter(FuturesContract.futures_id == self.id,
    #                                                     FuturesContract.listed_date >= day,
    #                                                     FuturesContract.expiration_date <= day
    #                                                     ).all()
    #
    # @property
    # def contract_size(self) -> str:
    #     return f'{self.size} {self.unit}'

    def __repr__(self):
        return f'<Futures(name={self.name},' \
               f'exchange={db_session.query(Exchange).filter_by(id=self.exchange_id).one().symbol},' \
               f'symbol={self.symbol})>'


class FuturesParameter(ModelBase):
    __tablename__ = 'futures'


class FuturesContract(ModelBase):
    __tablename__ = 'futures_contract'

    # 合约参数
    listing_date = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=False)
    first_delivery_day = Column(Date, nullable=False)
    last_delivery_day = Column(Date, nullable=False)
    benchmark_price = Column(Float, nullable=False)

    # 交易参数
    margin_rate_for_long_speculation = Column(Float, nullable=False)        # 投机买保证金率，>=1 为绝对值，<1为百分比。
    margin_rate_for_short_speculation = Column(Float, nullable=False)
    margin_rate_for_long_hedging = Column(Float, nullable=False)
    margin_rate_for_short_hedging = Column(Float, nullable=False)
    limit_up = Column(Float, nullable=False)
    limit_down = Column(Float, nullable=False)


# Trading Parameter
