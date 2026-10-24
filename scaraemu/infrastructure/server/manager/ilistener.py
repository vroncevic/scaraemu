# -*- coding: UTF-8 -*-

'''
Module
    ilistener.py
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
    Listener protocol for receiving virtual robot TCP server state updates.
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
class IServerStateListener(Protocol):
    '''
        Structural protocol for receiving virtual robot server lifecycle events.

        It defines:

            :methods:
                | on_server_state - Handles server running state and port updates.
                | get_version - Returns listener interface version.
    '''

    def on_server_state(self, running: bool, port: int) -> None:
        '''
            Handles server running state and port updates.

            :param running: True if server socket is actively listening, False otherwise.
            :param port: Bound TCP port number.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns listener interface version.

            :return: Semantic version string.
            :exceptions: None.
        '''
