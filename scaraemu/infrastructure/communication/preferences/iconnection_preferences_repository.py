# -*- coding: UTF-8 -*-

'''
Module
    iconnection_preferences_repository.py
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
    Interface protocol for storing and retrieving hardware communication settings.
'''

from __future__ import annotations

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
class IConnectionPreferencesRepository(Protocol):
    '''
        Storage protocol for persisting and reading hardware connection settings.

        It defines:

            :methods:
                | load_preference - Reads previously saved device endpoint and baudrate.
                | save_preference - Persists active device endpoint and baudrate to storage.
    '''

    def load_preference(self) -> tuple[str | None, int | None]:
        '''
            Reads previously saved device endpoint and baudrate.

            :return: Tuple of (port, baud) or (None, None) if not found.
            :exceptions: None.
        '''

    def save_preference(self, port: str, baud: int = 115200) -> bool:
        '''
            Persists active device endpoint and baudrate to storage.

            :param port: Device port identifier or network endpoint.
            :param baud: Communication baud rate integer.
            :return: True if persisted successfully, False otherwise.
            :exceptions: None.
        '''
