# -*- coding: UTF-8 -*-

'''
Module
    icli.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scaraemu is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scaraemu is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines interface ICLI for command-line interface adapters.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICLI(Protocol):
    '''
        Interface for command-line interface adapters.

        It defines:

            :methods:
                | is_initialized - Checks if the CLI adapter is initialized.
                | run - Executes CLI command line parsing and strategy dispatch.
    '''

    def is_initialized(self) -> bool:
        '''
            Checks if the CLI adapter is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''

    def run(self) -> Mapping[str, object]:
        '''
            Executes CLI command line parsing and strategy dispatch.

            :return: The execution result containing return code, stdout, and stderr.
            :exceptions: None.
        '''
