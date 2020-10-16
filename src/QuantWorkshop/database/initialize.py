# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import os
import csv

from QuantWorkshop.utility import packages_path_str
from .interface import db_session, db_engine
from .model import Exchange, ProductType


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


def init_product_type():
    csv_path: str = os.path.join(packages_path_str, 'database', 'data', 'product_type.csv')
    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            db_session.add(
                ProductType(
                    product_type=row['product_type'],
                    product_type_zh=row['product_type_zh']
                )
            )
    db_session.commit()


def initialize():
    initializer_dict: dict = {
        'Exchange': init_exchange,
        'ProductType': init_product_type,
    }

    for table, initializer in initializer_dict.items():
        if not db_engine.dialect.has_table(db_engine, globals()[table].__tablename__):
            globals()[table].__table__.create(bind = db_engine)
        initializer()
