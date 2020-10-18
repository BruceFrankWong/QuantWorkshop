# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'

"""
TDD for database module.

Test Requirements：
1) config
    1) The type of config variable is <dict> type;
    2) All keys in config is <str> type;
    3) Value types in config can be: <str> (including empty string), <dict> and <list>.

2) get_default_config:
    1) The type of return value is config, and its type is also <dict> type;

3) load_config:
    1) The config file is in json format;
    2) The config file is in path of current working directory;
    3) If config file does not exists, that means the first run. Make a default config file as a template;
    4) Load the json file, and return a valid <dict> (test in config).
"""

import os
import csv
from pathlib import Path

from QuantWorkshop.utility import packages_path_str
from QuantWorkshop.config import CONFIGS, generate_default_config, load_config
from QuantWorkshop.database import db_session, initialize, Exchange, Security


def test_initialize():
    initialize()


def test_exchange_and_security():
    exchange_name: str = '上交所'
    exchange: Exchange = db_session.query(Exchange).filter_by(name=exchange_name).one()
    result = db_session.query(Exchange).filter(Exchange.security_list.any(name_en='Stock')).all()
    print(result)
    print(Exchange.symbol_list())
    # element: ErExchangeAndSecurity
    # for element in exchange.security_list:
    #     print(element.exchange_id)
    #     print(type(element))


if __name__ == '__main__':
    test_initialize()
    test_exchange_and_security()
