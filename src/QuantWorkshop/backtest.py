# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


"""
Backtest module.
"""


import importlib
from datetime import date

from tqsdk import TqApi, TqAuth, TqBacktest, TqSim

from QuantWorkshop.config import CONFIGS
from QuantWorkshop.strategy import QWStrategyBase


def backtest(strategy: str, parameters: dict, symbol: str, capital: float, date_range: tuple):

    # 天勤量化
    tq_api: TqApi = TqApi(TqSim(capital),
                          auth=TqAuth(CONFIGS['tq_account'], CONFIGS['tq_password']),
                          backtest=TqBacktest(start_dt=date_range[0],
                                              end_dt=date_range[1]
                                              )
                          )

    # 动态加载策略。
    strategy_module = importlib.import_module(f'QuantWorkshop.strategy.{strategy}')
    strategy_object = getattr(strategy_module, strategy)
    strategy_instance: QWStrategyBase = strategy_object(tq_api, symbol, parameters)
    strategy_instance.run()
    print('strategy_module: ', type(strategy_module))
    print(type(strategy_object))
