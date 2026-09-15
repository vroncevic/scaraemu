# -*- coding: UTF-8 -*-

'''
Module
    serial_device_preferences.py
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
    Persistent store for saving and loading previously used serial device settings.
'''

from __future__ import annotations

from typing import ClassVar

from scaraemu.infrastructure.communication.preferences.connection_preferences_repository import (
    ConnectionPreferencesRepository,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialDevicePreferences:
    '''
        Persistent storage manager for last used serial communication device.

        It defines:

            :attributes:
                | _repository - Default connection preferences repository.
            :methods:
                | load_preference - Reads previously saved port and baud rate.
                | save_preference - Persists active port and baud rate to storage.
    '''

    _repository: ClassVar[ConnectionPreferencesRepository] = ConnectionPreferencesRepository()

    @classmethod
    def load_preference(cls) -> tuple[str | None, int | None]:
        '''
            Reads previously saved serial port and baud rate.

            :return: Tuple of (port, baud) or (None, None) if not found.
            :exceptions: None.
        '''
        return cls._repository.load_preference()

    @classmethod
    def save_preference(cls, port: str, baud: int = 115200) -> bool:
        '''
            Persists active port and baud rate to storage.

            :param port: Serial port identifier (e.g. '/dev/ttyACM0').
            :param baud: Communication baud rate integer.
            :return: True if persisted successfully, False otherwise.
            :exceptions: None.
        '''
        return cls._repository.save_preference(port, baud)
