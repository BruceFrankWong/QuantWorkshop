# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


"""
Strategy Module.
"""


from tqsdk import TqApi

from .base import QWStrategyBase


class ExampleStrategy(QWStrategyBase):
    """
    示例策略类。
    The example strategy class.
    """
    def __init__(self, api: TqApi, symbol: str, parameters: dict, mode):
        super().__init__(api=api, symbol=symbol, parameters=parameters, mode=mode)
        self.message: str = '其实这不是策略，这只是一个测试，用来验证 Python 动态加载。'

    def run(self):
        print(self.message)
        print(self.parameters['OK'])
