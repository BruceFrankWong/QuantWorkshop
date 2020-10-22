# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from pathlib import Path
import json


# The path of the packages <QuantWorkshop>
packages_path: Path = Path(__file__).parent
packages_path_str: str = str(packages_path)


def load_json(json_file: Path) -> dict:
    with open(json_file, mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def save_json(data: dict, json_file: Path) -> None:
    with open(json_file, mode='w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
