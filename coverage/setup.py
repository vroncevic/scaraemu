#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Module
    setup.py
Copyright
    Copyright (C) 2024 - 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    ats_coverage is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    ats_coverage is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines setup for package ats_coverage.
'''

from os.path import abspath, dirname, join
from setuptools import setup

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/ats_coverage'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/ats_coverage/blob/dev/LICENSE'
__version__: str = '5.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'

THIS_DIR: str = abspath(dirname(__file__))
long_description: str | None = None

with open(join(THIS_DIR, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()

PROGRAMMING_LANG: str = 'Programming Language :: Python ::'
VERSIONS: list[str] = ['3.12', '3.13', '3.14']
SUPPORTED_PY_VERSIONS: list[str] = [f'{PROGRAMMING_LANG} {VERSION}' for VERSION in VERSIONS]
PYP_CLASSIFIERS: list[str] = SUPPORTED_PY_VERSIONS

setup(
    name='ats_coverage',
    version='5.0.0',
    description='Python code coverage automation',
    author='Vladimir Roncevic',
    author_email='elektron.ronca@gmail.com',
    url='https://vroncevic.github.io/ats_coverage',
    license='GPL-3.0-or-later',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='code, coverage, automation',
    platforms='any',
    classifiers=PYP_CLASSIFIERS,
    py_modules=['ats_coverage', 'ats_updater'],
    install_requires=['ats_utilities', 'coverage'],
    data_files=[('', ['py.typed'])],
    entry_points={
        'console_scripts': [
            'ats_coverage=ats_coverage:main',
        ],
    }
)
