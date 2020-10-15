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
from pathlib import Path

from QuantWorkshop.config import CONFIGS, generate_default_config, load_config
from QuantWorkshop.database.initialize import initialize


def do_test():
    initialize()


if __name__ == '__main__':
    do_test()
