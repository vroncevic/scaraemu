# -*- coding: UTF-8 -*-

'''
Module
    itransport.py
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
    Defines abstract communication transport interface.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable, Callable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITransport(Protocol):
    '''
        Interface for communication transport layers (USB Serial, TCP Socket).

        It defines:

            :methods:
                | is_connected - Returns connection state.
                | connect - Establishes communication channel.
                | disconnect - Closes active connection.
                | write_line - Transmits string line packet.
                | set_callbacks - Registers asynchronous read and status logger callbacks.
    '''

    def is_connected(self) -> bool:
        '''
            Returns connection state.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        ...

    def connect(self, port: str, baudrate: int) -> bool:
        '''
            Establishes communication channel.

            :param port: Device address or port identifier.
            :param baudrate: Transmission baud rate.
            :return: True if connected successfully, False otherwise.
            :exceptions: None.
        '''
        ...

    def disconnect(self) -> None:
        '''
            Closes active connection.

            :exceptions: None.
        '''
        ...

    def write_line(self, data: str) -> bool:
        '''
            Transmits string line packet.

            :param data: Text payload to send.
            :return: True if transmitted, False otherwise.
            :exceptions: None.
        '''
        ...

    def set_callbacks(
        self,
        on_line: Callable[[str], None] | None = None,
        on_log: Callable[[str], None] | None = None
    ) -> None:
        '''
            Registers asynchronous read and status logger callbacks.

            :param on_line: Function invoked when new line is received.
            :param on_log: Function invoked for transport diagnostic messages.
            :exceptions: None.
        '''
        ...
