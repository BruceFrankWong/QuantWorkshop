# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


"""
Strategy Module.
"""

import abc

from tqsdk import TqApi


class QWStrategyBase(metaclass=abc.ABCMeta):
    """
    策略类的基类。
    The base of the strategy classes.
    """

    def __init__(self, api: TqApi, symbol: str, parameters: dict, mode):
        self.api: TqApi = api
        self.symbol: str = symbol
        self.parameters: dict = parameters
        self.mode = mode

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError
