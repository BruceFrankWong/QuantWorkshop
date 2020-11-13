# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict
import os
from pathlib import Path
import csv
import json

from QuantWorkshop.utility import packages_path_str


def load_json(json_file: Path) -> dict:
    with open(json_file, mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def save_json(data: dict, json_file: Path) -> None:
    with open(json_file, mode='w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_exchange() -> dict:
    csv_path: str = os.path.join(packages_path_str, 'initial_data', 'exchange.csv')
    result: Dict[str, Any] = {}
    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            result[row['symbol']] = {}
    return result


def read_futures() -> dict:
    json_path: Path = Path.cwd().joinpath(packages_path_str, 'initial_data', 'futures.json')
    if json_path.exists():
        return load_json(json_path)
    result: Dict[str, Any] = {}
    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            result[row['symbol']] = {}
    return result


if __name__ == '__main__':
    futures_list: dict = read_exchange()
    print(futures_list)
