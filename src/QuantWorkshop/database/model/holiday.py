# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List

from sqlalchemy import Table, Column, ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship

from ..interface import ModelBase, db_session


class Holiday(ModelBase):
    __tablename__ = 'holiday'

    id = Column(Integer, primary_key=True)
    begin = Column(Date, nullable=False)
    end = Column(Date, nullable=False)
    reason = Column(String)

    exchange_id = Column(Integer, ForeignKey('exchange.id'), nullable=False)

    exchange = relationship('Exchange', back_populates='holiday_list')

    def __repr__(self):
        return f'<Holiday(reason={self.reason}, begin={self.begin}, end={self.end})>'
