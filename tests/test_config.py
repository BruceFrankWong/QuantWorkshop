# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'

"""
TDD module for application path.

Requirements：
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


def do_test_for_config_item(value: tuple):
    """
    Test for requirements 1.2 and 1.3 .
    """
    assert isinstance(value[0], str)
    if isinstance(value[1], list):
        for element in value[1]:
            assert isinstance(element, dict)
            for sub_element in element.items():
                do_test_for_config_item(sub_element)
    elif isinstance(value[1], dict):
        for element in value[1].items():
            assert isinstance(element, tuple)
            do_test_for_config_item(element)
    else:
        assert len(value) == 2
        assert isinstance(value[1], str) or value[1] is None


def test_generate_default_config():
    """
    Test function <generate_default_config>.
    """
    config = generate_default_config()

    # test requirements 1.1, the type of <CONFIGS> should be <dict>.
    assert isinstance(config, dict) is True

    # call <do_test_for_config_item> to continue testing the others.
    for item in config.items():
        do_test_for_config_item(item)


def test_load_config_with_file_not_exist():
    """
    Test function <load_config>, with config file not exists.
    """
    cwd = Path.cwd()
    config_path = cwd.joinpath('config.json')

    if config_path.exists():
        os.remove(config_path)

    assert not config_path.exists()
    load_config()
    assert len(load_config()) > 0
    assert config_path.exists()


def test_load_config_with_file_exist():
    """
    Test function <load_config>, with config file exists.
    """
    cwd = Path.cwd()
    config_path = cwd.joinpath('config.json')

    if not config_path.exists():
        load_config()

    assert config_path.exists()
    config = load_config()
    assert len(config) > 0
    assert isinstance(config, dict)
    for item in config.items():
        do_test_for_config_item(item)


def test_config_variable():
    """
    Test variable <CONFIGS>.
    """
    # test requirements 1.1, the type of <CONFIGS> should be <dict>.
    assert isinstance(CONFIGS, dict) is True

    # call <do_test_for_config_item> to continue testing the others.
    for item in CONFIGS.items():
        do_test_for_config_item(item)
