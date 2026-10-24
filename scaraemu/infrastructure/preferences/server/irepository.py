# -*- coding: UTF-8 -*-

'''
Module
    irepository.py
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
    Interface protocol for storing and retrieving virtual manipulator TCP server settings.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.infrastructure.preferences.server.preference import ServerPreference

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IServerPreferenceRepository(Protocol):
    '''
        Storage protocol for persisting and reading virtual manipulator server network settings.

        It defines:

            :methods:
                | has_preference - Checks if valid stored preferences exist.
                | load_preference - Reads previously saved network host and port.
                | save_preference - Persists active network host and port to storage.
                | get_version - Returns interface version string.
    '''

    def has_preference(self) -> bool:
        '''
            Checks if valid stored server preferences exist.

            :return: True if preference file exists and is valid, False otherwise.
            :exceptions: None.
        '''

    def load_preference(self) -> ServerPreference:
        '''
            Reads previously saved network host and port.

            :return: ServerPreference value object.
            :exceptions: PreferenceNotFoundError.
        '''

    def save_preference(self, host: str, port: int = 8888) -> bool:
        '''
            Persists active network host and port to storage.

            :param host: Listening network host address.
            :param port: Listening TCP port number integer.
            :return: True if persisted successfully, False otherwise.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns interface version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
