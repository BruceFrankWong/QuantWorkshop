# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import os
import csv

from sqlalchemy.ext.declarative.api import DeclarativeMeta

from QuantWorkshop.utility import packages_path_str
from .interface import db_session, db_engine
from .model import Exchange, Security
from .model import relationship_table_exchange_and_security


def init_exchange():
    csv_path: str = os.path.join(packages_path_str, 'database', 'data', 'exchange.csv')
    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            db_session.add(
                Exchange(
                    symbol=row['symbol'],
                    name=row['name'],
                    fullname_zh=row['fullname_zh'],
                    fullname_en=row['fullname_en']
                )
            )
    db_session.commit()


def init_security():
    csv_path: str = os.path.join(packages_path_str, 'database', 'data', 'security.csv')
    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            db_session.add(
                Security(
                    name_en=row['name_en'],
                    name_zh=row['name_zh']
                )
            )
    db_session.commit()


def init_relationship_between_exchange_and_security():
    csv_path: str = os.path.join(packages_path_str, 'database', 'data', 'er_exchange_security.csv')
    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            exchange = db_session.query(Exchange).filter_by(symbol=row['exchange']).one()
            security = db_session.query(Security).filter_by(name_en=row['security']).one()
            exchange.security_list.append(security)
            db_session.commit()


def initialize():
    initializer_dict: dict = {
        'Exchange': init_exchange,
        'Security': init_security,
        'relationship_table_exchange_and_security': init_relationship_between_exchange_and_security,
    }

    for table, initializer in initializer_dict.items():
        so = globals()[table]
        if isinstance(so, DeclarativeMeta):
            if not db_engine.dialect.has_table(db_engine, so.__tablename__):
                so.__table__.create(bind=db_engine)
            initializer()
        else:
            if not db_engine.dialect.has_table(db_engine, table):
                so.create(bind=db_engine)
            initializer()

    # if not db_engine.dialect.has_table(db_engine, 'relationship_table_exchange_and_security'):
    #     relationship_table_exchange_and_security.

