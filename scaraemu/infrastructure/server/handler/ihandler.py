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
    Interface protocol for binary protocol frame command handlers.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.frame import BinaryFrame
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
class IBinaryCommandHandler(Protocol):
    '''
        Structural interface protocol for dedicated binary frame handlers.

        It defines:

            :methods:
                | can_handle - Checks whether handler processes the given message ID.
                | handle - Processes the binary frame and returns response frames.
                | get_version - Returns handler component version string.
    '''

    def can_handle(self, msg_id: MessageId) -> bool:
        '''
            Checks whether handler processes the given message ID.

            :param msg_id: Binary protocol MessageId enum value.
            :return: True if handler can process message ID, False otherwise.
            :exceptions: None.
        '''

    def handle(self, frame: BinaryFrame) -> list[BinaryFrame]:
        '''
            Processes the binary frame and produces response frames.

            :param frame: Decoded BinaryFrame from client.
            :return: List of response BinaryFrame instances.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns handler component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
