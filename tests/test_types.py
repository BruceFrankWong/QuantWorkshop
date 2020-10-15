# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'

"""
TDD for module <types.py>.

Test requirements:
1) config
    1) The type of config variable is <dict> type;
    2) All keys in config is <str> type;
    3) Value types in config can be: <str> (including empty string), <dict> and <list>.

2) get_default_config:
    1) The type of return value is config, and its type is also <dict> type;

3) load_config:
    1) The config file is in json format;
    2) The config file is in path of current working directory;
    3) If config file does not exists, that means the first run. Make a default config file as a template;
    4) Load the json file, and return a valid <dict> (test in config).
"""


import pytest

from QuantWorkshop.types import QWPeriodUnitType, QWPeriod


def test_period_unit_type():
    """
    Test to_second <generate_default_config> of class <QWPeriodUnitType>.
    """

    foo = QWPeriodUnitType.Tick
    assert foo.to_second() == 0
    assert foo.to_chinese() == 'Tick'

    foo = QWPeriodUnitType.Second
    assert foo.to_second() == 1
    assert foo.to_chinese() == '秒'

    foo = QWPeriodUnitType.Minute
    assert foo.to_second() == 60
    assert foo.to_chinese() == '分钟'

    foo = QWPeriodUnitType.Hour
    assert foo.to_second() == 60 * 60
    assert foo.to_chinese() == '小时'

    foo = QWPeriodUnitType.Day
    assert foo.to_second() == 60 * 60 * 24
    assert foo.to_chinese() == '日'

    foo = QWPeriodUnitType.Week
    assert foo.to_second() == 60 * 60 * 24 * 5
    assert foo.to_chinese() == '周'

    foo = QWPeriodUnitType.Month
    assert foo.to_second() == 60 * 60 * 24 * 5 * 4
    assert foo.to_chinese() == '月'

    foo = QWPeriodUnitType.Year
    assert foo.to_second() == 60 * 60 * 24 * 5 * 4 * 12
    assert foo.to_chinese() == '年'


def test_period_init():
    with pytest.raises(ValueError):
        foo = QWPeriod(frequency=0, unit=QWPeriodUnitType.Month)


@pytest.mark.parametrize(
    'frequency, unit, expected',
    [
        (1, QWPeriodUnitType.Tick, 0),
        (10, QWPeriodUnitType.Tick, 0),
        (1, QWPeriodUnitType.Second, 1),
        (70, QWPeriodUnitType.Second, 70),
        (70, QWPeriodUnitType.Minute, 60 * 70),
        (20, QWPeriodUnitType.Hour, 60 * 60 * 20),
        (5, QWPeriodUnitType.Day, 60 * 60 * 24 * 5),
        (2, QWPeriodUnitType.Week, 60 * 60 * 24 * 5 * 2),
        (3, QWPeriodUnitType.Month, 60 * 60 * 24 * 5 * 4 * 3),
        (8, QWPeriodUnitType.Year, 60 * 60 * 24 * 5 * 4 * 12 * 8),
    ]
)
def test_period_to_second(frequency: int, unit: QWPeriodUnitType, expected: int):
    foo = QWPeriod(frequency=frequency, unit=unit)
    assert foo.to_second() == expected
