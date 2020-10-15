# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


import os
import csv

from QuantWorkshop.utility import packages_path_str
from .interface import db_session
from .model import Exchange, ProductType


def init_exchange():
    csv_path: str = os.path.join(packages_path_str, 'database', 'data', 'exchange.csv')
    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            db_session.add(
                Exchange(
                    name=row['name'],
                    fullname=row['fullname'],
                    symbol=row['symbol']
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
                    name_en=row['name_en'],
                    name_zh=row['name_zh']
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
                    name_en=row['name_en'],
                    name_zh=row['name_zh']
                )
            )
    db_session.commit()
