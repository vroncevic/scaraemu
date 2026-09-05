# -*- coding: UTF-8 -*-

'''
Module
    ivirtual_robot_server.py
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
    Interface protocol for digital twin virtual robot TCP firmware emulator server.
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
class IVirtualRobotServer(Protocol):
    '''
        Protocol defining operations for a digital twin virtual robot TCP server.

        It defines:

            :methods:
                | start - Starts listening for external host connections.
                | stop - Terminates background server and closes client sockets.
                | is_running - Checks whether server is currently active.
                | get_port - Returns the active listening port number.
    '''

    def start(self, *, host: str = '127.0.0.1', port: int = 8888) -> bool:
        '''
            Starts listening for external host connections.

            :param host: Local IP bind address.
            :param port: TCP listening port number.
            :return: True if server started successfully, False otherwise.
            :exceptions: None.
        '''

    def stop(self) -> None:
        '''
            Terminates background server and closes client sockets.

            :exceptions: None.
        '''

    def is_running(self) -> bool:
        '''
            Checks whether server is currently active.

            :return: True if listening, False otherwise.
            :exceptions: None.
        '''

    def get_port(self) -> int:
        '''
            Returns the active listening port number.

            :return: Port integer.
            :exceptions: None.
        '''
