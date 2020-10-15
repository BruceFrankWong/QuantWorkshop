# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, String, Integer, Float, DateTime


ModelBase = declarative_base()


class Exchange(ModelBase):
    __tablename__ = 'exchange'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    fullname_zh = Column(String, nullable=False, unique=True)
    fullname_en = Column(String, nullable=False, unique=True)

    holiday_list = relationship('Holiday', back_populates='exchange')
    stock_list = relationship('Stock', back_populates='exchange')
    futures_list = relationship('Futures', back_populates='exchange')
    option_list = relationship('Option', back_populates='exchange')

    def __repr__(self):
        return f'<Exchange(name={self.name}, fullname={self.fullname}, abbr={self.symbol})>'


class ProductType(ModelBase):
    __tablename__ = 'product_type'

    id = Column(Integer, primary_key=True)
    name_en = Column(String, nullable=False, unique=True)
    name_zh = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f'<ProductType(name_en={self.name_en}, name_zh={self.name_zh})>'


table_exchange_product = Table()
