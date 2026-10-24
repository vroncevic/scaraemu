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
    Interface protocol for dispatching binary frames in virtual robot server.
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
class IServerFrameDispatcher(Protocol):
    '''
        Interface protocol for processing and routing server binary frame payloads.

        It defines:

            :methods:
                | dispatch_binary - Parses raw bytes into frames and returns packed response bytes.
                | reset - Resets underlying protocol parsers and command state.
                | get_version - Returns protocol specification version.
    '''

    def dispatch_binary(self, data: bytes) -> tuple[bytes, ...]:
        '''
            Parses raw bytes into binary frames, processes them, and returns encoded response bytes.

            :param data: Incoming raw byte buffer.
            :return: Sequence of packed binary frame response payloads.
            :exceptions: None.
        '''

    def reset(self) -> None:
        '''
            Resets underlying protocol parsers and command state.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol specification version.

            :return: Semantic version string.
            :exceptions: None.
        '''
