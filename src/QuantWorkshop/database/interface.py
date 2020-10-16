# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from sqlalchemy import create_engine, event, MetaData, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from QuantWorkshop.utility import packages_path_str
from QuantWorkshop.config import CONFIGS


def db_engine_sqlite():
    return create_engine(f'sqlite:///{packages_path_str}/{CONFIGS["database"]["database"]}')


def db_engine_postgresql():
    return create_engine(
        'postgresql+psycopg2:///{user}:{password}@{host}:{port}/{database}'.format(
            user=CONFIGS['database']['user'],
            password=CONFIGS['database']['password'],
            host=CONFIGS['database']['host'],
            port=CONFIGS['database']['port'],
            database=CONFIGS['database']['database'],
        )
    )


def get_db_engine():
    generator: dict = {
        'sqlite': db_engine_sqlite,
        'postgresql': db_engine_postgresql,
    }
    return generator[CONFIGS['database']['driver']]()


db_engine = get_db_engine()
db_session = sessionmaker(bind=db_engine)()

ModelBase = declarative_base()
