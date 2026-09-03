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

import json
import os
from pathlib import Path
from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialDevicePreferences:
    '''
        Persistent storage manager for last used serial communication device.

        It defines:

            :attributes:
                | CONFIG_DIR - Directory path for configuration storage.
                | CONFIG_FILE - File path to the serial device configuration JSON.
            :methods:
                | load_preference - Reads previously saved port and baud rate.
                | save_preference - Persists active port and baud rate to storage.
    '''

    CONFIG_DIR: ClassVar[Path] = Path(os.path.expanduser('~/.config/scara'))
    CONFIG_FILE: ClassVar[Path] = Path(os.path.expanduser('~/.config/scara/serial_device.json'))

    @classmethod
    def load_preference(cls) -> tuple[str | None, int | None]:
        '''
            Reads previously saved serial port and baud rate.

            :return: Tuple of (port, baud) or (None, None) if not found.
            :exceptions: None.
        '''
        try:
            if cls.CONFIG_FILE.is_file():
                with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as stream:
                    payload: dict[str, object] = json.load(stream)
                    raw_port = payload.get('port')
                    raw_baud = payload.get('baud')
                    port: str | None = str(raw_port) if raw_port is not None else None
                    baud: int | None = int(raw_baud) if raw_baud is not None else None
                    return port, baud
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            pass
        return None, None

    @classmethod
    def save_preference(cls, port: str, baud: int = 115200) -> bool:
        '''
            Persists active port and baud rate to storage.

            :param port: Serial port identifier (e.g. '/dev/ttyACM0').
            :param baud: Communication baud rate integer.
            :return: True if persisted successfully, False otherwise.
            :exceptions: None.
        '''
        if not port or port == 'Virtual / None':
            return False
        try:
            cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as stream:
                json.dump({'port': port, 'baud': baud}, stream, indent=2)
            return True
        except (OSError, TypeError):
            return False
