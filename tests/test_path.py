# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


"""
TDD module for application path.

Request：
*) Query the absolute path for package <QuantWorkshop>, that means the <application_path> variable。
"""


import pytest

import os.path
from QuantWorkshop.utility import application_path


def test_application_path():
    assert str(application_path) == os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    pytest.main()
