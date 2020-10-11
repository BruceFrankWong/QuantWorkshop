# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


"""
TDD module for application path.

Request：
*) Query the absolute path for package <QuantWorkshop>, that means the <application_path> variable。
"""


import os.path
import QuantWorkshop
from QuantWorkshop.utility import application_path


def test_application_path():
    assert str(application_path) == os.path.dirname(QuantWorkshop.__file__)
