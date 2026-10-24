# -*- coding: UTF-8 -*-

'''
Module
    ihandler.py
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
    Interface protocol for hardware serial response and telemetry demultiplexers.
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
class IResponseHandler(Protocol):
    '''
        Interface protocol for hardware serial response and telemetry demultiplexers.

        It defines:

            :methods:
                | on_bytes - Processes received raw bytes and updates telemetry.
                | on_log - Processes transport diagnostic message.
                | get_version - Returns protocol specification version.
    '''

    def on_bytes(self, data: bytes) -> None:
        '''
            Processes received raw byte buffer and dispatches demultiplexed responses.

            :param data: Received raw byte payload.
            :exceptions: None.
        '''

    def on_log(self, message: str) -> None:
        '''
            Processes transport diagnostic message.

            :param message: Diagnostic log message string.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol specification version.

            :return: Semantic version string.
            :exceptions: None.
        '''
