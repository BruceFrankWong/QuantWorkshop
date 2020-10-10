#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages


def get_version_string():
    with open('QuantWorkshop/__init__.py', 'r') as f:
        version_line = re.search(
            r'__version__\s+=\s+(.*)', f.read()
        ).group(1)
    return version_line


setup(
    name='QuantWorkshop',
    version=get_version_string(),
    description='This is a test of the setup',
    long_description='long_description',
    long_description_content_type="text/markdown",
    url="https://github.com/kenblikylee/imgkernel",
    author='Bruce Frank Wong',
    author_email='Bruce.Frank.Wong@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=open('requirements.txt').read().splitlines(),
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
