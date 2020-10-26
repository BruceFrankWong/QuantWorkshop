# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Optional, Tuple
from datetime import datetime

import pandas as pd
import mplfinance as mpf

from QuantWorkshop.config import CONFIGS
from QuantWorkshop.utility import packages_path_str


def plot(df: pd.DataFrame,
         title: Optional[str] = None,
         mav: Optional[Tuple[int]] = None,
         alines: Optional[dict] = None):
    color = mpf.make_marketcolors(up='red', down='cyan', inherit=True)
    # style = mpf.make_mpf_style(marketcolors=color, rc={'axes.facecolor': '#eee8d5'})#fdf6e3
    style = mpf.make_mpf_style(marketcolors=color, rc={'axes.facecolor': '#fdf6e3'})

    # # 设置外观效果
    # plt.rc('font', family='Microsoft YaHei')  # 用中文字体，防止中文显示不出来
    # plt.rc('figure', fc='k')  # 绘图对象背景图
    # plt.rc('text', c='#800000')  # 文本颜色
    # plt.rc('axes', axisbelow=True, xmargin=0, fc='k', ec='#800000', lw=1.5, labelcolor='#800000',
    #        unicode_minus=False)  # 坐标轴属性(置底，左边无空隙，背景色，边框色，线宽，文本颜色，中文负号修正)
    # plt.rc('xtick', c='#d43221')  # x轴刻度文字颜色
    # plt.rc('ytick', c='#d43221')  # y轴刻度文字颜色
    # plt.rc('grid', c='#800000', alpha=0.9, ls=':', lw=0.8)  # 网格属性(颜色，透明值，线条样式，线宽)
    # plt.rc('lines', lw=0.8)  # 全局线宽
    #
    # # 创建绘图对象和4个坐标轴
    # figure = plt.figure(figsize=(16, 8))
    # left, width = 0.01, 0.98
    # ax1 = figure.add_axes([left, 0.6, width, 0.35])  # left, bottom, width, height
    # ax2 = figure.add_axes([left, 0.45, width, 0.15], sharex=ax1)  # 共享ax1轴
    # ax3 = figure.add_axes([left, 0.25, width, 0.2], sharex=ax1)  # 共享ax1轴
    # ax4 = figure.add_axes([left, 0.05, width, 0.2], sharex=ax1)  # 共享ax1轴
    # plt.setp(ax1.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示
    # plt.setp(ax2.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示
    # plt.setp(ax3.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示
    #
    # # 绘制蜡烛图
    # mpf.c(ax, data['open'], data['close'], data['high'], data['low'],
    #                       width=0.5, colorup='r', colordown='green',
    #                       alpha=0.6)

    filename: str = f'Test_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'
    kwargs: dict = {
        'type': 'candle',
        'style': style,
        'volume': False,
        'figratio': (3, 1),
        'figscale': 20,
        'savefig': dict(fname=f'{packages_path_str}\\{CONFIGS["picture_path"]}\\{filename}',
                        bbox_inches='tight'
                        )
    }
    if title:
        kwargs['title'] = title
    if mav:
        kwargs['mav'] = mav
    if alines:
        kwargs['alines'] = alines

    mpf.figure()
    mpf.plot(df, **kwargs)
    mpf.show()
