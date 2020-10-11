# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict
import json
from pathlib import Path

from QuantWorkshop.utility import load_json, save_json


def generate_default_config() -> dict:
    """
    Generate a default config template.
    """
    return {
        # 路径
        'data_downloaded': 'data_downloaded',
        'picture_path': 'picture',

        # 数据库
        'database': {
            'driver': 'sqlite',
            'host': '',
            'port': '',
            'database': 'QuantWorkshop.sqlite',
            'user': '',
            'password': '',
        },

        # 天勤量化
        'tq': {
            'account': '',
            'password': '',
        },

        # 交易账户
        'transaction': [
            {
                'broker': '',
                'account': '',
                'password': '',
            }
        ]
    }


def load_config() -> dict:
    """
    Load the <config.json> from the current working directory, and return the config variable.
    """
    config_path: Path = Path.cwd().joinpath('config.json')
    if config_path.exists():
        return load_json(config_path)
    else:
        print('File <config.json> not found.')
        print('Maybe it is your first run this application, we generate a <config.json> file with the default value.')
        print('Change the value as yours.')
        save_json(generate_default_config(), config_path)
        return generate_default_config()


def save_config() -> None:
    """
    Save the config variable into the <config.json> which exists in the current working directory.
    """
    global CONFIGS
    file_path: Path = Path.cwd().joinpath('config.json')
    with open(file_path, mode='w+', encoding='utf-8') as f:
        json.dump(CONFIGS, f, indent=4, ensure_ascii=False)


# The config variable.
CONFIGS: Dict[str, Any] = load_config()
