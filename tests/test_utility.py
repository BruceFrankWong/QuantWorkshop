# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


"""
TDD module for application path.

Request：
1) Query the absolute path for package <QuantWorkshop>, that means the <packages_path> variable。

2) load_json:
    1) raise an exception if file not found;
    2)
"""


import os.path

import QuantWorkshop
from QuantWorkshop.utility import packages_path


def test_packages_path():
    assert str(packages_path) == os.path.dirname(QuantWorkshop.__file__)
