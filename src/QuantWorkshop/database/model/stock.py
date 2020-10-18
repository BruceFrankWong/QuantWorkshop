# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List
from datetime import date

from sqlalchemy import Table, Column, ForeignKey, String, Integer, Float, Date, Time, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from ..interface import ModelBase, db_session
from .exchange import Exchange


class Stock(ModelBase):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)

    exchange_id = Column(Integer, ForeignKey('exchange.id'), nullable=False)

    exchange = relationship('Exchange', back_populates='stock_list')

    def __repr__(self):
        return f'<Stock(symbol={self.symbol}, name={self.name})>'
