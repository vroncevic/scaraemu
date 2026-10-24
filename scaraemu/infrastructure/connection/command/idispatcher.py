# -*- coding: UTF-8 -*-

'''
Module
    idispatcher.py
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
    Interface protocol for hardware binary command dispatching and queue clearing.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.message import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICommandDispatcher(Protocol):
    '''
        Structural protocol defining binary command dispatch and buffer flushes.

        It defines:

            :methods:
                | send_command - Transmits a binary protocol command frame to hardware.
                | clear_queue - Flushes pending host queue and resets flow control.
                | get_version - Returns interface version string.
    '''

    def send_command(self, msg_id: MessageId, payload: bytes = b'') -> None:
        '''
            Transmits a binary protocol command frame to hardware.

            :param msg_id: Binary protocol MessageId identifier.
            :param payload: Optional packed command payload bytes.
            :exceptions: None.
        '''

    def clear_queue(self) -> None:
        '''
            Flushes pending host queue and resets flow control.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns interface version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
